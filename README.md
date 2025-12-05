# API de Gestión de Biblioteca — Tarea 2

Bases de Datos II — Ingeniería en Computación e Informática

Estudiante: Guillermo Vargas
Docente: Diego Álvarez S.

## Cambios Implementados 

**Diseño e Implementación — Punto 1 (Category + relación Book–Category)**

* Se creó el modelo Category con atributos id, name y description.

* Se implementó la relación many-to-many con Book mediante la tabla intermedia books_categories.

* Se configuraron las relaciones ORM en ambos modelos.

* Se generó y aplicó una migración completa con Alembic incluyendo tabla, índices y FK.

* Se crearon los DTOs:

  * CategoryReadDTO

  * CategoryCreateDTO

  * CategoryUpdateDTO

* Se implementó CategoryRepository siguiendo el patrón repositorio.

* Se creó CategoryController con CRUD completo.

* Se agregó endpoint para asignar categorías a un libro.

***Decisiones de diseño relevantes***

* Se utilizó relationship(..., secondary=...) en ambos modelos para mantener sincronía ORM.

* Los DTO excluyen campos de auditoría y relaciones para evitar sobreexposición de datos.

* Se centralizó la inyección de repositorios usando Provide, manteniendo cohesión con el diseño base del proyecto.

* Se usaron validaciones mínimas en DTOs según lo exigido en la guía, dejando validaciones complejas a controladores.

* Las migraciones se generaron siguiendo la estructura Alembic existente para evitar inconsistencias.

**Diseño e Implementación — Punto 2 (Review + validaciones)**

* Se creó el modelo Review con los atributos: id, review_text, rating, review_date, book_id (FK), user_id (FK).

* Se implementaron las relaciones ORM correspondientes:

  * Review.book → Book.reviews

  * Review.user → User.reviews

* Se generó y aplicó la migración Alembic creando la tabla reviews con llaves foráneas, índices y restricciones necesarias.

* Se crearon los DTOs:

  * ReviewReadDTO

  * ReviewCreateDTO

  * ReviewUpdateDTO

* Se implementó ReviewRepository siguiendo el patrón de repositorio del proyecto, asegurando coherencia con los repositorios existentes.

* Se creó ReviewController, incluyendo CRUD completo y validaciones específicas:

  * Validación de rating entre 1 y 5.

  * Validación de máximo 3 reseñas por usuario por libro.

  * Asignación automática de review_date = date.today() al crear una reseña.

* Se integró el controlador en la aplicación registrando sus rutas bajo /reviews.

* Decisiones de diseño relevantes

* Se aplicaron validaciones simples desde los DTOs y validaciones más complejas a nivel controlador, siguiendo las pautas del enunciado.

* Se utilizó get_and_update() y operaciones ORM directas para mantener integridad en actualizaciones parciales.

**Diseño e Implementación — Punto 3 (Extensión del modelo Book)**

* Se agregaron los nuevos campos al modelo Book: stock, description, language, publisher.

* Se definió stock con valor por defecto 1 y como campo obligatorio.

* El campo language se limitó a códigos ISO 639-1 de 2 letras.

* Se creó y aplicó una migración Alembic que añade los nuevos campos a la tabla books.

* Se actualizaron los DTOs de creación y actualización para incluir los nuevos atributos.

* En POST /books se agregaron validaciones:

  * stock > 0

  * language ∈ {es, en, fr, de, it, pt}

* En PATCH /books/{id} se validó que:

  * stock no sea negativo

  * language siga el conjunto permitido

***Decisiones de diseño relevantes***

* Se mantuvo la estructura del ORM y el patrón repositorio para coherencia del proyecto.

* Las validaciones se resolvieron en el controlador para centralizar la lógica de negocio.

* Los valores por defecto y restricciones se definieron tanto en el modelo como en la migración para asegurar consistencia entre aplicación y base de datos.

**Actualización del modelo User - Punto 4**

* Se agregaron los nuevos campos: email, phone, address (opcional) e is_active (por defecto True).

* Se creó la migración correspondiente usando Alembic.

* Se actualizó el UserReadDTO para excluir correctamente password y loans.

* En los endpoints de crear y actualizar, se agregó validación de formato de correo mediante expresión regular.

* El campo is_active fue bloqueado en los DTOs de creación y actualización para evitar que el usuario lo modifique directamente.

## Cumplimiento de Requerimientos - Tarea 2

| Nº | Requerimiento | Estado | 
| :---: | :--- | :---: |
| **1** | Crear modelo Category + relación many-to-many con Book | **CUMPLIDO** | 
| **2** | Crear modelo Review con relaciones y validaciones | **CUMPLIDO** |
| **3** | Actualizar modelo Book con inventario, descripción y validaciones | **CUMPLIDO** |
| **4** | Actualizar modelo User (email, phone, address, is_active) | **CUMPLIDO** |
| **5** | Actualizar modelo Loan con due_date, fine_amount y LoanStatus | **** |
| **6** | Implementar métodos avanzados en BookRepository + endpoints | **** |
| **7** | Implementar métodos en LoanRepository + endpoints | **** |
| **8** | Crear base de datos inicial + initial_data.sql | **** |




# API con Litestar y PostgreSQL

API REST para gestión de biblioteca que permite administrar usuarios, libros y préstamos. Incluye autenticación JWT y documentación interactiva (Swagger/Scalar).

## Requisitos

- [uv](https://github.com/astral-sh/uv)
- PostgreSQL

## Inicio rápido

```bash
uv sync                      # Instala las dependencias
cp .env.example .env         # Configura las variables de entorno (ajusta según sea necesario)
uv run alembic upgrade head  # Aplica las migraciones de la base de datos
uv run litestar --reload     # Inicia el servidor de desarrollo
# Accede a http://localhost:8000/schema para ver la documentación de la API
```

## Variables de entorno

Crea un archivo `.env` basado en `.env.example`:

- `DEBUG`: Modo debug (True/False)
- `JWT_SECRET_KEY`: Clave secreta para tokens JWT
- `DATABASE_URL`: URL de conexión a PostgreSQL (formato: `postgresql+psycopg://usuario:contraseña@host:puerto/nombre_bd`). Recuerda crear la base de datos antes de ejecutar la aplicación con `createdb nombre_bd`.

## Estructura del proyecto

```
app/
├── controllers/     # Endpoints de la API (auth, book, loan, user)
├── dtos/            # Data Transfer Objects
├── repositories/    # Capa de acceso a datos
├── models.py        # Modelos SQLAlchemy (User, Book, Loan)
├── db.py            # Configuración de base de datos
├── config.py        # Configuración de la aplicación
└── security.py      # Autenticación y seguridad
migrations/          # Migraciones de Alembic
```

## Crear una copia privada de este repositorio

Para crear una copia privada de este repositorio en tu propia cuenta de GitHub, conservando el historial de commits, sigue estos pasos:

- Primero, crea un repositorio privado en tu cuenta de GitHub. Guarda la URL del nuevo repositorio.
- Luego, ejecuta los siguientes comandos en tu terminal, reemplazando `<URL_DE_TU_REPOSITORIO_PRIVADO>` con la URL de tu nuevo repositorio privado:

  ```bash
  git clone https://github.com/dialvarezs/learning-vue-bd2-2025 # Clona el repositorio
  cd learning-vue-bd2-2025
  git remote remove origin                                      # Elimina el origen remoto existente
  git remote add origin <URL_DE_TU_REPOSITORIO_PRIVADO>         # Agrega el nuevo origen remoto
  git push -u origin main                                       # Sube la rama principal al
  ```
