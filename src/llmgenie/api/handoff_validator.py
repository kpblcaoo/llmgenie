"""
Handoff validation module for llmgenie
Implements automated completeness validation for context transfer packages
Based on 016_context_transfer_protocol atomic rule
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from datetime import datetime
from pathlib import Path
import json
import os

# Pydantic models for handoff validation
class HandoffFile(BaseModel):
    """Single file in handoff package"""
    path: str = Field(..., description="File path relative to project root")
    type: str = Field(..., description="File type: summary, lessons, checklist, audit, metadata")
    priority: int = Field(..., description="Priority order (1=highest)")
    exists: bool = Field(default=False, description="Whether file exists")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")

class StartupPrompt(BaseModel):
    """Startup prompt validation"""
    includes_status: bool = Field(default=False, description="Includes current status")
    includes_infrastructure: bool = Field(default=False, description="Includes infrastructure info")
    includes_lessons: bool = Field(default=False, description="Includes lessons learned")
    includes_constraints: bool = Field(default=False, description="Includes scope constraints")
    includes_next_steps: bool = Field(default=False, description="Includes next steps")

class ControlQuestions(BaseModel):
    """Control questions validation"""
    questions_provided: bool = Field(default=False, description="Control questions provided")
    question_count: int = Field(default=0, description="Number of questions")
    covers_status: bool = Field(default=False, description="Questions cover status")
    covers_technical: bool = Field(default=False, description="Questions cover technical details")
    covers_scope: bool = Field(default=False, description="Questions cover scope understanding")

class HandoffPackage(BaseModel):
    """Complete handoff package for validation"""
    from_role: str = Field(..., description="Source role (e.g., 'coder', 'reviewer')")
    to_role: str = Field(..., description="Target role (e.g., 'librarian', 'auditor')")
    epic_id: str = Field(..., description="Epic/session identifier")
    files: List[HandoffFile] = Field(..., description="Files in package")
    startup_prompt: str = Field(..., description="Proposed startup prompt")
    control_questions: List[str] = Field(..., description="Control questions for verification")
    success_criteria: List[str] = Field(..., description="Success criteria for continuation")
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")

class ValidationResult(BaseModel):
    """Handoff validation result"""
    is_valid: bool = Field(..., description="Overall validation result")
    completeness_score: float = Field(..., description="Completeness score 0.0-1.0")
    
    # Detailed validation results
    file_validation: Dict[str, bool] = Field(..., description="Per-file validation results")
    prompt_validation: StartupPrompt = Field(..., description="Startup prompt validation")
    questions_validation: ControlQuestions = Field(..., description="Control questions validation")
    
    # Issues and recommendations
    missing_files: List[str] = Field(default_factory=list, description="Missing required files")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")
    
    # Metadata
    validated_at: datetime = Field(default_factory=datetime.now, description="Validation timestamp")
    validator_version: str = Field(default="1.0.0", description="Validator version")

class HandoffValidator:
    """Core handoff validation logic"""
    
    REQUIRED_FILE_TYPES = [
        "summary",      # Quick overview/status
        "lessons",      # Detailed lessons learned
        "checklist",    # Original checklist with progress
        "audit",        # Technical/audit report  
        "metadata"      # Project state/metadata
    ]
    
    MIN_FILES_COUNT = 5
    MIN_QUESTIONS_COUNT = 3
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
    
    def validate_package(self, package: HandoffPackage) -> ValidationResult:
        """Validate complete handoff package"""
        
        # File validation
        file_validation = self._validate_files(package.files)
        missing_files = self._find_missing_files(package.files)
        
        # Prompt validation  
        prompt_validation = self._validate_startup_prompt(package.startup_prompt)
        
        # Questions validation
        questions_validation = self._validate_control_questions(package.control_questions)
        
        # Calculate completeness score
        completeness_score = self._calculate_completeness_score(
            file_validation, prompt_validation, questions_validation
        )
        
        # Generate warnings and recommendations
        warnings = self._generate_warnings(package, file_validation, prompt_validation, questions_validation)
        recommendations = self._generate_recommendations(package, missing_files, warnings)
        
        # Overall validation
        is_valid = (
            len(package.files) >= self.MIN_FILES_COUNT and
            all(file_validation.values()) and
            completeness_score >= 0.8 and
            len(missing_files) == 0
        )
        
        return ValidationResult(
            is_valid=is_valid,
            completeness_score=completeness_score,
            file_validation=file_validation,
            prompt_validation=prompt_validation,
            questions_validation=questions_validation,
            missing_files=missing_files,
            warnings=warnings,
            recommendations=recommendations
        )
    
    def _validate_files(self, files: List[HandoffFile]) -> Dict[str, bool]:
        """Validate individual files in package"""
        validation = {}
        
        for file in files:
            file_path = self.project_root / file.path
            exists = file_path.exists()
            
            # Update file object
            file.exists = exists
            if exists:
                file.size_bytes = file_path.stat().st_size
            
            # Basic validation: file exists and has content
            validation[file.path] = exists and (file.size_bytes or 0) > 0
        
        return validation
    
    def _find_missing_files(self, files: List[HandoffFile]) -> List[str]:
        """Find missing required file types"""
        provided_types = {f.type for f in files}
        missing_types = set(self.REQUIRED_FILE_TYPES) - provided_types
        return list(missing_types)
    
    def _validate_startup_prompt(self, prompt: str) -> StartupPrompt:
        """Validate startup prompt content"""
        prompt_lower = prompt.lower()
        
        return StartupPrompt(
            includes_status="status" in prompt_lower or "статус" in prompt_lower,
            includes_infrastructure="infrastructure" in prompt_lower or "инфраструктура" in prompt_lower,
            includes_lessons="lessons" in prompt_lower or "уроки" in prompt_lower,
            includes_constraints="scope" in prompt_lower or "ограничения" in prompt_lower,
            includes_next_steps="next steps" in prompt_lower or "следующие шаги" in prompt_lower
        )
    
    def _validate_control_questions(self, questions: List[str]) -> ControlQuestions:
        """Validate control questions"""
        question_text = " ".join(questions).lower()
        
        return ControlQuestions(
            questions_provided=len(questions) > 0,
            question_count=len(questions),
            covers_status="status" in question_text or "статус" in question_text,
            covers_technical="test" in question_text or "тест" in question_text,
            covers_scope="scope" in question_text or "готов" in question_text
        )
    
    def _calculate_completeness_score(
        self, 
        file_validation: Dict[str, bool], 
        prompt_validation: StartupPrompt,
        questions_validation: ControlQuestions
    ) -> float:
        """Calculate overall completeness score"""
        
        # File score (50% of total)
        file_score = sum(file_validation.values()) / max(len(file_validation), 1) if file_validation else 0
        
        # Prompt score (30% of total)  
        prompt_checks = [
            prompt_validation.includes_status,
            prompt_validation.includes_infrastructure,
            prompt_validation.includes_lessons,
            prompt_validation.includes_constraints,
            prompt_validation.includes_next_steps
        ]
        prompt_score = sum(prompt_checks) / len(prompt_checks)
        
        # Questions score (20% of total)
        questions_checks = [
            questions_validation.questions_provided,
            questions_validation.question_count >= self.MIN_QUESTIONS_COUNT,
            questions_validation.covers_status,
            questions_validation.covers_technical,
            questions_validation.covers_scope
        ]
        questions_score = sum(questions_checks) / len(questions_checks)
        
        return 0.5 * file_score + 0.3 * prompt_score + 0.2 * questions_score
    
    def _generate_warnings(
        self, 
        package: HandoffPackage,
        file_validation: Dict[str, bool],
        prompt_validation: StartupPrompt,
        questions_validation: ControlQuestions
    ) -> List[str]:
        """Generate validation warnings"""
        warnings = []
        
        if len(package.files) < self.MIN_FILES_COUNT:
            warnings.append(f"Minimum {self.MIN_FILES_COUNT} files required, found {len(package.files)}")
        
        if not all(file_validation.values()):
            failed_files = [path for path, valid in file_validation.items() if not valid]
            warnings.append(f"Files not found or empty: {', '.join(failed_files)}")
        
        if not prompt_validation.includes_status:
            warnings.append("Startup prompt missing status information")
        
        if questions_validation.question_count < self.MIN_QUESTIONS_COUNT:
            warnings.append(f"Minimum {self.MIN_QUESTIONS_COUNT} control questions required")
        
        return warnings
    
    def _generate_recommendations(
        self, 
        package: HandoffPackage,
        missing_files: List[str],
        warnings: List[str]
    ) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if missing_files:
            recommendations.append(f"Add missing file types: {', '.join(missing_files)}")
        
        if len(warnings) > 0:
            recommendations.append("Address validation warnings before handoff")
        
        recommendations.append("Verify all files contain current and relevant information")
        recommendations.append("Test startup prompt in clean environment before handoff")
        
        return recommendations 