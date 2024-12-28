import os
import json

from pathlib import Path
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from pydantic import Json

class CertificateManager():
  def __init__(self, base_dir: str = "/etc/orbit/certstore"):
    self.base_dir = Path(base_dir)
    self.metadata_file = self.base_dir / "metadata.json"
    self.csr_dir = self.base_dir / "csr"
    self.cert_dir = self.base_dir / "cert"

    self.metadata = {}

    try:
      self.base_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
      print(f"Error creating directory {str(self.base_dir)}: {e}")

    try:
      self.csr_dir.mkdir(parents=False, exist_ok=True)
    except OSError as e:
      print(f"Error creating directory {str(self.csr_dir): {e}}")

    try:
      self.cert_dir.mkdir(parents=False, exist_ok=True)
    except OSError as e:
      print(f"Error creating directory {str(self.cert_dir)}: {e}")

    if not self.metadata_file.exists():
      self._initialize_metadata()
    else:
      try:
        with open(self.metadata_file, 'r') as f:
          self.metadata = json.load(f.read())

  def _initialize_metadata(self):
    try:
      with open(self.metadata_file, "w") as f:
        json.dump({}, f, indent=4)
    except OSError:
      print(f"Error initializing metadata file {str(self.metadata_file)}")

  def add_csr(self, data: str = None, cn: str = "localhost", verify: bool = True, overwrite: bool = False):
    verified = False

    target = self.csr_dir / f"{cn}.csr"
    
    if verify:
      try:
        csr = x509.load_pem_x509_csr(data=data, backend=default_backend())
      except ValueError:
        return False
      
      try:
        subject = csr.subject
        csr_cn = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)

        if csr_cn == cn and csr_cn != "" or csr_cn != None and cn != "" or cn != None:
          verified = True
        else:
          print(f"CSR verification failed CN={csr_cn} does not match provided CN={cn}")
          return False
        
      except Exception as e:
        print(f"Failed to extract CN from CSR: {e}")
        return False
      
    if verified is True or verify is False:
      if self.csr_dir.exists():
        if not target.exists() or overwrite is True:
          with open(str(target), "wb") as f:
            f.write(data)
        else:
          print(f"File {str(target)} already exist and overwrite is not set.")
          return False
      else:
        print(f"Directory {str(self.csr_dir)} was expected to exist but doesn't.")
        return False

  def _save_metadata(self):
    try:
      with open(str(self.metadata_file), 'wb') as f:
        f.write(json.dump(self.metadata))
    except OSError as e:
      print(f"Error saving metadata to file: {e}")
      return False
    
    return True
  
  def _update_metadata(self, key: str, data: dict):
      self.metadata[key] = data

      return self._save_metadata()
    
  def get_metadata(self, key: str) -> dict:
    return self.metadata.get(key)
  
  

    
        



      
      
    