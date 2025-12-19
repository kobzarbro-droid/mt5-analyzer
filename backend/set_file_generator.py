"""
MT5 .set File Generator
Generates MT5 preset files (.set) for quick loading into tester
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class SetFileGenerator:
    """Generator for MT5 .set preset files"""
    
    @staticmethod
    def generate_set_file(parameters: Dict[str, Any], preset_name: str = "preset") -> str:
        """
        Generate MT5 .set file content
        
        Args:
            parameters: Dictionary of parameter names and values
            preset_name: Name of the preset
            
        Returns:
            Content of the .set file as string
        """
        logger.info(f"Generating .set file for preset: {preset_name}")
        
        # MT5 .set file format
        lines = [
            "; saved automatically on " + datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
            "; this file contains last used input parameters for testing/optimizing " + preset_name + " expert advisor",
            ";"
        ]
        
        # Add each parameter
        for param_name, param_value in parameters.items():
            # Determine parameter type and format
            if isinstance(param_value, bool):
                value_str = "true" if param_value else "false"
                param_type = "bool"
            elif isinstance(param_value, int):
                value_str = str(param_value)
                param_type = "int"
            elif isinstance(param_value, float):
                value_str = f"{param_value:.8f}"
                param_type = "double"
            elif isinstance(param_value, str):
                value_str = param_value
                param_type = "string"
            else:
                value_str = str(param_value)
                param_type = "string"
            
            # Format: parameter_name=value||type||description
            lines.append(f"{param_name}={value_str}||{param_type}||")
        
        content = "\n".join(lines)
        logger.info(f"Generated .set file with {len(parameters)} parameters")
        
        return content
    
    @staticmethod
    def parse_set_file(content: str) -> Dict[str, Any]:
        """
        Parse MT5 .set file content
        
        Args:
            content: Content of the .set file
            
        Returns:
            Dictionary of parameter names and values
        """
        logger.info("Parsing .set file")
        
        parameters = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith(';'):
                continue
            
            # Parse parameter line
            if '=' in line:
                parts = line.split('=', 1)
                param_name = parts[0].strip()
                
                # Split value and type
                value_parts = parts[1].split('||')
                value_str = value_parts[0].strip()
                param_type = value_parts[1].strip() if len(value_parts) > 1 else 'string'
                
                # Convert value based on type
                if param_type == 'bool':
                    param_value = value_str.lower() == 'true'
                elif param_type == 'int':
                    try:
                        param_value = int(value_str)
                    except:
                        param_value = 0
                elif param_type == 'double':
                    try:
                        param_value = float(value_str)
                    except:
                        param_value = 0.0
                else:
                    param_value = value_str
                
                parameters[param_name] = param_value
        
        logger.info(f"Parsed .set file with {len(parameters)} parameters")
        return parameters
