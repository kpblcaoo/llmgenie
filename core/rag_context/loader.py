"""Загрузчики для правил и структуры проекта"""

import json
import fnmatch
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from bs4 import BeautifulSoup, Comment


@dataclass
class Document:
    """Унифицированный документ для RAG системы"""
    content: str
    source: str  # путь к файлу
    doc_type: str  # "rule" или "struct"
    metadata: Dict[str, Any]  # дополнительные метаданные


class RulesLoader:
    """Загрузчик правил из .cursor/rules"""
    
    def __init__(self, rules_dir: Path, extensions: List[str], exclude_patterns: List[str]):
        self.rules_dir = rules_dir
        self.extensions = extensions
        self.exclude_patterns = exclude_patterns
    
    def load_documents(self) -> List[Document]:
        """Загружает все правила как документы"""
        documents = []
        
        if not self.rules_dir.exists():
            return documents
        
        for file_path in self._get_rule_files():
            try:
                doc = self._parse_rule_file(file_path)
                if doc:
                    documents.append(doc)
            except Exception as e:
                print(f"Warning: Не удалось загрузить правило {file_path}: {e}")
        
        return documents
    
    def _get_rule_files(self) -> List[Path]:
        """Получает список файлов правил"""
        files = []
        
        for pattern in [f"*{ext}" for ext in self.extensions]:
            files.extend(self.rules_dir.glob(pattern))
            files.extend(self.rules_dir.rglob(pattern))  # рекурсивно
        
        # Фильтруем исключения
        filtered_files = []
        for file_path in files:
            should_exclude = False
            for exclude_pattern in self.exclude_patterns:
                if fnmatch.fnmatch(file_path.name, exclude_pattern):
                    should_exclude = True
                    break
            
            if not should_exclude:
                filtered_files.append(file_path)
        
        return list(set(filtered_files))  # убираем дубли
    
    def _parse_rule_file(self, file_path: Path) -> Optional[Document]:
        """Парсит отдельный файл правил"""
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Базовая очистка markdown 
            clean_content = self._clean_markdown(content)
            
            # Извлекаем метаданные из заголовка
            metadata = self._extract_metadata(content)
            metadata.update({
                "file_size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
                "extension": file_path.suffix
            })
            
            return Document(
                content=clean_content,
                source=str(file_path),
                doc_type="rule",
                metadata=metadata
            )
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def _clean_markdown(self, content: str) -> str:
        """Базовая очистка markdown для лучшего embedding"""
        # Убираем избыточные символы
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Пропускаем пустые строки и комментарии
            if line.strip() and not line.strip().startswith('<!--'):
                # Убираем markdown синтаксис
                clean_line = line.replace('**', '').replace('*', '').replace('`', '')
                clean_line = clean_line.replace('##', '').replace('#', '')
                cleaned_lines.append(clean_line.strip())
        
        return '\n'.join(cleaned_lines)
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Извлекает метаданные из содержимого"""
        metadata = {}
        
        lines = content.split('\n')
        for line in lines[:10]:  # смотрим только первые 10 строк
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
            elif '- role:' in line:
                metadata['role'] = line.split('role:')[1].strip()
            elif '- applies to:' in line:
                metadata['applies_to'] = line.split('applies to:')[1].strip()
        
        return metadata


class StructLoader:
    """Загрузчик структуры проекта из struct.json"""
    
    def __init__(self, struct_json: Path):
        self.struct_json = struct_json
    
    def load_document(self) -> Optional[Document]:
        """Загружает struct.json как документ"""
        if not self.struct_json.exists():
            return None
        
        try:
            with open(self.struct_json, 'r', encoding='utf-8') as f:
                struct_data = json.load(f)
            
            # Создаем читаемое представление структуры
            content = self._format_struct_content(struct_data)
            
            metadata = {
                "file_size": self.struct_json.stat().st_size,
                "modified": self.struct_json.stat().st_mtime,
                "components_count": len(struct_data.get("components", {})),
                "endpoints_count": len(struct_data.get("endpoints", {}))
            }
            
            return Document(
                content=content,
                source=str(self.struct_json),
                doc_type="struct",
                metadata=metadata
            )
            
        except Exception as e:
            print(f"Error loading struct.json: {e}")
            return None
    
    def _format_struct_content(self, struct_data: Dict[str, Any]) -> str:
        """Форматирует struct.json в читаемый текст"""
        content_parts = []
        
        # Основная информация
        if "project" in struct_data:
            content_parts.append(f"Project: {struct_data['project'].get('name', 'Unknown')}")
            content_parts.append(f"Description: {struct_data['project'].get('description', '')}")
        
        # Компоненты
        if "components" in struct_data:
            content_parts.append("\nComponents:")
            for comp_name, comp_data in struct_data["components"].items():
                content_parts.append(f"- {comp_name}: {comp_data.get('description', '')}")
                if "capabilities" in comp_data:
                    for cap in comp_data["capabilities"]:
                        content_parts.append(f"  * {cap}")
        
        # Endpoints
        if "endpoints" in struct_data:
            content_parts.append("\nAPI Endpoints:")
            for endpoint, ep_data in struct_data["endpoints"].items():
                method = ep_data.get("method", "GET")
                desc = ep_data.get("description", "")
                content_parts.append(f"- {method} {endpoint}: {desc}")
        
        return '\n'.join(content_parts) 