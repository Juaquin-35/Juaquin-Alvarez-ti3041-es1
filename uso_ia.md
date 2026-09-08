Anexo: Declaración de Uso de Inteligencia Artificial

Parte 1: Declaración de Uso de IA
-Herramienta utilizada: Gemini (Google DeepMind)
-Propósito del uso:
    -Asistencia en el diseño de arquitectura general para un catálogo en Django basado en archivos JSON y sin base de datos.
    -Orientación en la estructuración de la entrega por etapas y definición de puntos de commit para control de versiones en Git.
    -Depuración de errores de configuración (TemplateDoesNotExist y reestructuración de rutas en plantillas).
    -Refactorización y limpieza de código en el controlador (catalogo/views.py).
    -Generación y enriquecimiento de datos (productos.json) con 40 productos e integración de imágenes mediante URLs de Unsplash.
    -Integración de imágenes web en la interfaz frontend (lista.html y detalle.html).

Parte 2: Registro de Prompts y Evolución del Proyecto
1. Requerimientos Generales y Planificación (Prompt Raíz)
-Prompt de entrada:
    "Estoy creando un sistema de catalogo para una ferreteria (sección A de la parte de proyecto Transversal catalogo online en el pdf) en la cual todos los detalles que debe de llevar este sistema de catalogo estan en el pdf adjunto esto debe de ser desarrollado de manera en la que no use una base de datos, solo datos mediante JSON y se especifica que tambien haya commits en ciertas partes del desarrollo las cuales van separados entonces lo ideal seria que vayas especificando donde se hace commit y documentar las funciones importantes este proyecto tambien va con diseño front end el cual debes de utilizar css y html y el formato general del proyecto es en Django"

-Respuesta / Solución aplicada:
    -Se definió la estructura de un proyecto Django que lee datos desde un archivo estático catalogo/data/productos.json usando json.load().
    -Se diseñó la ruta de desarrollo dividida en 5 etapas (etapa-0-entorno, etapa-1-app, etapa-2-interfaz, etapa-3-mejoras y entrega-final) asociadas a sus respectivos commits.
    -Se estructuraron las vistas principales y las plantillas base en HTML/CSS.

2. Configuración de URLs en la Etapa 1
-Prompt de entrada:
    "en la etapa 1 como va ordenado todo en url.py"

-Respuesta / Solución aplicada:
    -Se explicó la separación entre el archivo de enrutamiento global (config/urls.py usando include) y el archivo local (catalogo/urls.py) para servir la aplicación desde la raíz.

3. Aclaración sobre Importaciones
-Prompt de entrada:
    "el import en views debo borrar el que esta por defecto?"

-Respuesta / Solución aplicada:
    -Se aclaró que convenía mantener from django.shortcuts import render para su posterior uso al conectar plantillas HTML en la Etapa 2.

4. Verificación y Despliegue Local
-Prompt de entrada:
    "luego de completar todas las etapas como inicio la app"

-Respuesta / Solución aplicada:
    -Se indicaron los comandos para activar el entorno (python -m pipenv shell) y ejecutar el servidor local (python manage.py runserver) para validar la navegación de la app.

5. Corrección del Error TemplateDoesNotExist
-Prompt de entrada:
    -"TemplateDoesNotExist" / "esta es la estructura [Imagen adjunta de VS Code]"

-Respuesta / Solución aplicada:
    -Se diagnosticó que la carpeta templates estaba en la raíz del proyecto. Se reubicó dentro de catalogo/templates/catalogo/ para cumplir con la convención de búsqueda de plantillas de Django.

6. Refactorización y Limpieza de Vistas
-Prompt de entrada:
    "todo esto esta en views [Código con funciones duplicadas]"

-Respuesta / Solución aplicada:
    -Se eliminaron duplicidades en el archivo catalogo/views.py, consolidando la función lista_productos junto con la lógica para calcular la métrica de productos con y sin stock.

7. Integración de Imágenes Web en el Catálogo
-Prompt de entrada:
    "lo que necesito ahora es colocar imagenes de acorde a cada herramienta... no es necesario que sean imagenes locales pueden ser imagenes ubicadas en la web... podrias ayudarme a colocarle imagen a cada uno de los productos?"

-Respuesta / Solución aplicada:
    -Se actualizó el archivo catalogo/data/productos.json incorporando la propiedad "imagen" con enlaces directos de Unsplash para los 40 productos.
    -Se modificaron las plantillas lista.html y detalle.html para desplegar las imágenes en tarjetas y en la vista detallada de forma dinámica.