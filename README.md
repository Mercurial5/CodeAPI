# CodeAPI

## .env 

#### Main keys:
> `LANGUAGES_PATH`: Path to the folder where all languages will store their temporary-code. Can be written with respective to the current working directory.

> `PATH_TO_HOST_VOLUME`: Full path to the `LANGUAGES_PATH`.

> `PATH_TO_CONTAINER_VOLUME`: Root (First in path) directory must be the same as in image.

#### Better use this keys:
> `CASE_DELIMITER`: Special symbols to separate test runs from one another.

> `TIMEOUT_ERROR_MESSAGE`: Special symbols to indicate timeout error.

#### Api keys:
> `FLASK_HOST`: Host.

> `FLASK_PORT`: Port. 