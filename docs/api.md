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
                "url": "/f/4.jpg",
                "size": 341717,
                "date": "2014-12-08 11:21:49.881686+01:00",
                "hash": "XAU7IM+LXlpWROLbW9iz574gOLTCWhmSwUJLuMWpBXHKlPW/9mm9t/OytbW1sLR+z777G+Ut+D1j4OA4B2eNQw==",
                "expires": null,
                "extension": ".jpg",
                "id": 4
            }
        ]
    }

* *original_filename*  
  Original name, string.
* *url*  
  Relative url to a file, string.
* *size*  
  File size in bytes, integer.
* *date*  
  Upload date, ISO 8601 formatted string.
* *hash*  
  File hash, base64 encoded SHA-512, string.
* *expires*  
  Expiration date, ISO 8601 formatted string or null.
* *extension*  
  File extension prefixed with a dot, string.
* *id*  
  File id.

#### Exceptions
In case of an exception an additional key called `files` will be present
containing information about the files which were uploaded successfully, just as
shown above, as well as the usual key `message`.


### /file/info [GET]
Returns information about a file.

#### Arguments
* *id*  
  File id.

#### Response
Identical to the response produced by `/file/upload`.

#### Exceptions
Additional HTTP status codes which may be encountered: `400` (id not an
integer), `404` (no file with that id).


### /stats [GET]
Returns statistics.

#### Arguments
None.

#### Response

    {
        "total_size": 1342478,
        "total_files": 4
    }

* *total_size*  
  Size of all files in bytes, integer.
* *total_files*  
  Number of all files, integer.

#### Exceptions.
Default.
