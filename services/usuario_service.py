import hashlib

from typing import Optional

from repositories import usuario_repo
from models.usuario_model import UsuarioModel

class UsuarioService:

    def __init__(self, session):
        self.session = session

    @staticmethod
    def hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str):
        usuario = usuario_repo.get_by_usuarioName(self.session, username)

        if not usuario:
            return None  # usuario no existe
        
        if usuario.activo == 0:
            return "NO ACTIVO"  # usuario NO ACTIVO
        
        if usuario.clave != self.hash_password(password):
            return False  # contraseña incorrecta

        return usuario  # autenticación OK
    
    def get_by_usuario(self, updateUser: UsuarioModel) -> Optional[UsuarioModel]:
        usuario = usuario_repo.get_by_usuarioName(self.session, updateUser.usuario)
        if not usuario:
            return None
        
        return usuario
    
    def actualizar_clave(self, updateUser: UsuarioModel) -> Optional[UsuarioModel]:
        usuario = usuario_repo.get_by_idUsuario(self.session, updateUser.idUsuario)
        if not usuario:
            return None
        
        usuario.clave = updateUser.clave
        
        return usuario_repo.update(self.session, usuario)
    
    def actualizar_fechaUltimoLogin(self, updateUser: UsuarioModel) -> Optional[UsuarioModel]:
        usuario = usuario_repo.get_by_idUsuario(self.session, updateUser.idUsuario)
        if not usuario:
            return None
        
        usuario.fechaUltimoLogin = updateUser.fechaUltimoLogin
        
        return usuario_repo.update(self.session, usuario)