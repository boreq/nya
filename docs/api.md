# API
All api urls start with `/api`, for example `/api/file/upload`.

## Errors
Encountered errors are indicated with an appropriate status code and a response
in a following format:

    {
        "message": "No file with such id."
    }

* *message*  
    Human readable message.

Default HTTP status code of an exception is `500` and may always be encountered,
additional status codes are mentioned in the individual *Exceptions* sections.

## Urls

### /file/upload [POST]
Uploads a file.

#### Arguments
* *file*  
  File(s) to upload.
* *expires*  
  How long the files should be kept on a server [seconds]. Set to `0` to keep
  files forever.

#### Response

    {
        "files": [
            {
                "original_filename": "my_file.jpg",
                "url": "/f/ed32d332d04614ac5af4ae28101ec8.jpg",
                "filename": "ed32d332d04614ac5af4ae28101ec8.jpg",
                "expires": 300
            }
        ]
    }

* *original_filename*  
  Original name, string.
* *url*  
  Relative url to a file, string.
* *filename*  
    Filename, string.
* *expires*  
  Expiration time in seconds.

#### Exceptions
In case of an exception an additional key called `files` will be present
containing information about the files which were uploaded successfully, just as
shown above, as well as the usual key `message`.

### /stats [GET]
Returns statistics.

#### Arguments
None.

#### Response

    {
        "redis_number_of_keys": 2, 
        "redis_peak_memory": 9670472, 
        "redis_peak_memory_human": "9.22M", 
        "redis_used_memory": 579504, 
        "redis_used_memory_human": "565.92K"
    }

* *redis_number_of_keys*  
  Number of keys in redis, integer.
* *redis_peak_memory*  
  Peak memory used by redis, bytes, integer.
* *redis_peak_memory_human*  
  Peak memory used by redis, human readable, string.
* *redis_used_memory*  
  Memory used by redis, bytes, integer.
* *redis_used_memory_human*  
  Memory used by redis, human readable, string.

#### Exceptions.
Default.
