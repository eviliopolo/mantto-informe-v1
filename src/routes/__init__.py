# Rutas

from .auth_routes import router as auth_routes  
from .obligaciones_routes import router as obligaciones_routes
from .inventario_routes import router as inventario_routes
from .comunicados_routes import router as comunicados_routes
from .seccion1_routes import router as seccion1_routes
from .section2_routes import router as section2_routes
from .seccion3_routes import router as seccion3_routes
from .seccion4_routes import router as seccion4_routes
from .seccion5_routes import router as seccion5_routes

routes = [
    auth_routes,
    obligaciones_routes,
    inventario_routes,
    comunicados_routes,
    seccion1_routes,
    section2_routes,
    seccion3_routes,
    seccion4_routes,
    seccion5_routes
]

