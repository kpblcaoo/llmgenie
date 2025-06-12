"""Configuration loader for llmgenie.

Loads configuration from multiple layers:
1. defaults.json - base configuration
2. profiles/{profile}.json - profile-specific settings
3. project_overrides/{project}.json - project-specific overrides
4. Environment variables (LLMGENIE_*)
5. CLI arguments

Copyright (C) 2025 Mikhail Stepanov
Licensed under GPL v3+
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Configuration loading error."""
    pass


class ConfigLoader:
    """Hierarchical configuration loader for llmgenie."""
    
    def __init__(self, config_root: Optional[Union[str, Path]] = None):
        """Initialize config loader.
        
        Args:
            config_root: Root directory for configuration files.
                        Defaults to 'config/' relative to project root.
        """
        if config_root is None:
            # Find project root by looking for pyproject.toml
            current = Path.cwd()
            while current != current.parent:
                if (current / "pyproject.toml").exists():
                    config_root = current / "config"
                    break
                current = current.parent
            else:
                # Fallback to current directory
                config_root = Path.cwd() / "config"
        
        self.config_root = Path(config_root)
        self._cache = {}
        
    def load_config(
        self,
        profile: str = "dev",
        project: Optional[str] = None,
        config_path: Optional[str] = None,
        cli_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load complete configuration from all layers.
        
        Args:
            profile: Profile name (dev, tool, prod)
            project: Project name for project-specific overrides
            config_path: Manual config file path (overrides all)
            cli_overrides: CLI argument overrides
            
        Returns:
            Complete merged configuration
        """
        if config_path:
            return self._load_manual_config(config_path, cli_overrides)
            
        # Load configuration layers
        config = {}
        
        # Layer 1: Defaults
        defaults = self._load_defaults()
        config = self._deep_merge(config, defaults)
        
        # Layer 2: Profile
        profile_config = self._load_profile(profile)
        config = self._deep_merge(config, profile_config)
        
        # Layer 3: Project overrides
        if project:
            project_config = self._load_project_overrides(project)
            config = self._deep_merge(config, project_config)
        
        # Layer 4: Environment variables
        env_config = self._load_env_vars()
        config = self._deep_merge(config, env_config)
        
        # Layer 5: CLI overrides
        if cli_overrides:
            config = self._deep_merge(config, cli_overrides)
            
        # Add metadata
        config["_metadata"] = {
            "profile": profile,
            "project": project,
            "config_root": str(self.config_root),
            "loaded_layers": self._get_loaded_layers(profile, project)
        }
        
        return config
    
    def _load_defaults(self) -> Dict[str, Any]:
        """Load base defaults configuration."""
        defaults_path = self.config_root / "defaults.json"
        return self._load_json_file(defaults_path, required=True)
    
    def _load_profile(self, profile: str) -> Dict[str, Any]:
        """Load profile-specific configuration."""
        profile_path = self.config_root / "profiles" / f"{profile}.json"
        profile_config = self._load_json_file(profile_path, required=False)
        
        if not profile_config:
            logger.warning(f"Profile '{profile}' not found, using defaults only")
            return {}
            
        # Handle 'extends' directive
        if "extends" in profile_config:
            base_profile = profile_config["extends"]
            if base_profile != "defaults":
                base_config = self._load_profile(base_profile)
                profile_config = self._deep_merge(base_config, profile_config)
        
        # Apply overrides if present
        if "overrides" in profile_config:
            overrides = profile_config.pop("overrides")
            profile_config = self._deep_merge(profile_config, overrides)
            
        return profile_config
    
    def _load_project_overrides(self, project: str) -> Dict[str, Any]:
        """Load project-specific configuration overrides."""
        project_path = self.config_root / "project_overrides" / f"{project}.json"
        project_config = self._load_json_file(project_path, required=False)
        
        if not project_config:
            logger.info(f"No project overrides found for '{project}'")
            return {}
            
        # Handle 'extends' directive for project configs
        if "extends" in project_config:
            base_profile = project_config["extends"]
            base_config = self._load_profile(base_profile)
            # Don't merge base profile, just use as reference
            
        # Apply overrides if present
        if "overrides" in project_config:
            overrides = project_config.pop("overrides")
            project_config = self._deep_merge(project_config, overrides)
            
        return project_config
    
    def _load_env_vars(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {}
        
        # Map environment variables to config paths
        env_mappings = {
            "LLMGENIE_PROFILE": "llmgenie.default_profile",
            "LLMGENIE_LOG_LEVEL": "llmgenie.logging.level",
            "LLMGENIE_LOG_OUTPUT": "llmgenie.logging.output",
            "LLMGENIE_PROJECTS_DIR": "llmgenie.workspace.projects_dir",
            "LLMGENIE_DEFAULT_MODEL": "llmgenie.ai_models.default",
            "LLMGENIE_TEMPERATURE": "llmgenie.ai_models.temperature",
            "LLMGENIE_MAX_TOKENS": "llmgenie.ai_models.max_tokens",
        }
        
        for env_var, config_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(env_config, config_path, value)
                
        return env_config
    
    def _load_manual_config(
        self, 
        config_path: str, 
        cli_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Load configuration from manually specified file."""
        config = self._load_json_file(Path(config_path), required=True)
        
        if cli_overrides:
            config = self._deep_merge(config, cli_overrides)
            
        config["_metadata"] = {
            "manual_config": config_path,
            "loaded_layers": ["manual", "cli_overrides"] if cli_overrides else ["manual"]
        }
        
        return config
    
    def _load_json_file(self, path: Path, required: bool = False) -> Dict[str, Any]:
        """Load JSON file with error handling."""
        if not path.exists():
            if required:
                raise ConfigurationError(f"Required configuration file not found: {path}")
            return {}
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in {path}: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading {path}: {e}")
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result
    
    def _set_nested_value(self, config: Dict[str, Any], path: str, value: str):
        """Set nested configuration value from dot-separated path."""
        keys = path.split('.')
        current = config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
            
        # Try to convert value to appropriate type
        final_value = self._convert_env_value(value)
        current[keys[-1]] = final_value
    
    def _convert_env_value(self, value: str) -> Union[str, int, float, bool]:
        """Convert environment variable string to appropriate type."""
        # Boolean conversion
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
            
        # Number conversion
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
            
        # Return as string
        return value
    
    def _get_loaded_layers(self, profile: str, project: Optional[str]) -> list:
        """Get list of loaded configuration layers."""
        layers = ["defaults"]
        
        if profile:
            layers.append(f"profile:{profile}")
            
        if project:
            layers.append(f"project:{project}")
            
        layers.extend(["env_vars", "cli_overrides"])
        return layers
    
    def get_project_config_path(self, project: str) -> Path:
        """Get path to project-specific configuration."""
        return self.config_root / "project_overrides" / f"{project}.json"
    
    def get_project_state_path(self, project: str) -> Path:
        """Get path to project state file."""
        # Find project root
        current = Path.cwd()
        while current != current.parent:
            if (current / "pyproject.toml").exists():
                return current / "projects" / project / "project_state.json"
            current = current.parent
        
        # Fallback
        return Path.cwd() / "projects" / project / "project_state.json"
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure."""
        required_keys = ["llmgenie"]
        
        for key in required_keys:
            if key not in config:
                raise ConfigurationError(f"Missing required configuration key: {key}")
                
        llmgenie_config = config["llmgenie"]
        required_llmgenie_keys = ["version", "mode"]
        
        for key in required_llmgenie_keys:
            if key not in llmgenie_config:
                raise ConfigurationError(f"Missing required llmgenie configuration key: {key}")
                
        return True


def load_config(
    profile: str = "dev",
    project: Optional[str] = None,
    config_path: Optional[str] = None,
    cli_overrides: Optional[Dict[str, Any]] = None,
    config_root: Optional[str] = None
) -> Dict[str, Any]:
    """Convenience function to load configuration.
    
    Args:
        profile: Profile name (dev, tool, prod)
        project: Project name for project-specific overrides
        config_path: Manual config file path (overrides all)
        cli_overrides: CLI argument overrides
        config_root: Root directory for configuration files
        
    Returns:
        Complete merged configuration
    """
    loader = ConfigLoader(config_root)
    return loader.load_config(profile, project, config_path, cli_overrides)


def get_project_paths(project: str, config_root: Optional[str] = None) -> Dict[str, Path]:
    """Get all relevant paths for a project.
    
    Args:
        project: Project name
        config_root: Root directory for configuration files
        
    Returns:
        Dictionary with project paths
    """
    loader = ConfigLoader(config_root)
    
    # Find project root
    current = Path.cwd()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            project_root = current
            break
        current = current.parent
    else:
        project_root = Path.cwd()
    
    return {
        "project_root": project_root,
        "projects_dir": project_root / "projects",
        "project_dir": project_root / "projects" / project,
        "project_config": loader.get_project_config_path(project),
        "project_state": loader.get_project_state_path(project),
        "config_root": loader.config_root
    } 