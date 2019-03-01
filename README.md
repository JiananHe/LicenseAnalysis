# LicenseAnalysis
Analysis the compliance and conflicts of various open-source licenses.
## Dependencies
* Python 3.6.*
* Django 2.1.*
* pandas
### change Django source code:
Go to the source code folder of Django package(it should be ***python_path/Lib/site-packages/django/***), find the file ***core/files/uploadedfile.py***, then change the ***_set_name() function in UploadedFile class***:
```python
    def _set_name(self, name):
    #    # Sanitize the file name so that it can't be dangerous.
    #    if name is not None:
    #        # Just use the basename of the file -- anything else is dangerous.
    #        name = os.path.basename(name)

    #        # File names longer than 255 characters can cause problems on older OSes.
    #        if len(name) > 255:
    #            name, ext = os.path.splitext(name)
    #            ext = ext[:255]
    #            name = name[:255 - len(ext)] + ext

        self._name = name
```
Just comment out all code except the last line. We make these changes to get the full absolute path of uploaded file.


## Startup
* Go to the folder where manage.py exists, then run Python command:
```Python
python manage.py runserver <IP>:<PORT>
```
If there are no errors, then you have started your web server successfully.<br>
* Open your browser, input the url:
```
<IP>:<PORT>/license
```

