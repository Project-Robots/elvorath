from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse

router = APIRouter(
  prefix="/orbit-ca/v1",
  tags=["certificate_authority"],
  responses={404: {"description": "Not found"}},
)

@router.get("/")
async def orbit_ca():
  return PlainTextResponse(content="Orbit CA v1", status_code=200)

@router.get("/status")
async def ca_status():
  return PlainTextResponse(content="Healthy", status_code=200)

@router.get("/certificiate/{node_name}")
async def get_certificate(node_name: str):
  if node_name is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate")
  
  return PlainTextResponse(content="Certificate", status_code=200)

@router.get("/certificate_request/{node_name}")
async def get_csr(node_name: str):
  if node_name is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_request")
  
  return PlainTextResponse(content="Certificate Signing Request", status_code=200)

@router.put("/certificate_request/{node_name}")
async def save_csr(node_name: str):
  if node_name is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_request")

  return PlainTextResponse(content="Certificate Request Saved.", status_code=201)

@router.get("/certificate_status/{certname}")
async def get_status(certname: str):
  if certname is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_status")
  
  return JSONResponse(content={}, status_code=200)

@router.put("/certificate_status/{certname}")
async def save_status(certname: str):
  if certname is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_status")
  
  return JSONResponse(content={}, status_code=201)

@router.delete("/certificate_status/{certname}")
async def delete_certificate_data(certname: str):
  if certname is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_status")
  
  return JSONResponse(content={"state": "deleted"}, status_code=200)

@router.get("/certificate_statuses/{key}")
async def get_statuses(key: str):
  if key is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/certificate_statuses")
  
  return JSONResponse(content={}, status_code=200)

@router.get("/certificate_revocation_list/ca")
async def certificate_revocation_list():
  return PlainTextResponse(content="Certificate Revocation List in PEM format", status_code=200)


@router.get("/expirations/{certname}")
async def expirations(certname: str):
  if certname is None:
    return HTTPException(400, "No request key specified in /orbit-ca/v1/expirations")
  
  return PlainTextResponse(content="List of expirations by certname.", status_code=200)

@router.put("/clean")
async def clean():
  PlainTextResponse(content="Successfully cleaned all certificates", status_code=200)
