import os
from pathlib import Path
from configparser import ConfigParser, MissingSectionHeaderError, NoOptionError, NoSectionError

class ConfigManager:
  def __init__(self):
    self.config = ConfigParser()
    self.expected_schema = {
      "uvicorn": ["ssl_key", "ssl_cert", "ssl_ca_chain", "workers", "listen", "port", "log_level"],
      "certificate_authority": ["datastore_dir", "autosign", "verify_signature", "verify_expiration"]
    }
    self.default_paths = [
      Path(os.getenv("ELVORATH_CONFIG", "")),
      Path.home() / ".orbit" / "elvorath.conf",
      Path("/etc/orbit/elvorath.conf")
    ]
    self.load_config()

  def load_config(self):
    for path in self.default_paths:
      if path.exists():
        try:
          self.config.read(path)
          self.validate_config()
          print("Loaded config from", path)
          return
        except (MissingSectionHeaderError, NoOptionError, NoSectionError) as e:
          print("Error loading config from", path, ":", e)

    raise FileNotFoundError("No config file found")
  
  def validate_config(self):
      for section in self.expected_schema:
        if section not in self.config.sections():
          raise ValueError(f"Missing section {section} in config")

        for option in self.expected_schema[section]:
          if option not in self.config[section]:
            raise ValueError(f"Missing option {option} in section {section}")

  
  def get(self, section, key, fallback=None, type_cast=None):
    try:
      value = self.config.get(section, key, fallback=fallback)
      if type_cast:
        return type_cast(value)
      return value
    except (NoOptionError, NoSectionError):
      return fallback
    

config = ConfigManager()