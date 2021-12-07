from fastapi import APIRouter
from controllers import clienteController, enderecoController, pontoController, contratoController, contratoEventoController

router = APIRouter()

#CLIENTES
router.include_router(clienteController.router, prefix="/api/v1/clientes")
#FIM CLIENTES

#ENDEREÇOS 
router.include_router(enderecoController.router, prefix="/api/v1/enderecos")
#FIM ENDEREÇOS

#PONTO
router.include_router(pontoController.router, prefix="/api/v1/pontos")
#FIM PONTO

#CONTRATOS
router.include_router(contratoController.router, prefix="/api/v1/contratos")
#FIM CONTRATOS

#HISTORICO
router.include_router(contratoEventoController.router, prefix="/api/v1/contrato")
#FIM HISTORICO
