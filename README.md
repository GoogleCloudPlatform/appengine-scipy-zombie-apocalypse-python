Copyright (C) 2010-2014 Google Inc.
# App Engine Python VM Runtime 'Zombie Apocalypse' example

This sample is inspired by a [Zombie Apocalypse ODEINT demo][1] listed
in the [Scipy Cookbook][2].

It demos use of the `apt_get_install` directive in the `app.yaml` file to load `python-numpy`, `python-scipy`, and `python-matplotlib`.

## Deploying

1. Make sure that you are invited to the [VM Runtime Trusted Tester
   Program][3], and [download the SDK](http://commondatastorage.googleapis.com/gae-vm-runtime-tt/vmruntime_sdks.html).
2. Update the `application` value of the `app.yaml` file from
   `your-app-id` to the Application ID which is whitelisted for the VM
   Runtime Trusted Tester Program.
3. Run the following command:

   ```
   $ <sdk_directory>/appcfg.py -s preview.appengine.google.com update <project_directory>
   ```

4. Visit the following URL:
   `http://your-app-id.appspot.com/`


## Contributing changes

* See [CONTRIB.md](CONTRIB.md)


## Licensing

* See [LICENSE](LICENSE)


[1]: http://wiki.scipy.org/Cookbook/Zombie_Apocalypse_ODEINT
[2]: http://wiki.scipy.org/Cookbook/
[3]: https://docs.google.com/document/d/1VH1oVarfKILAF_TfvETtPPE3TFzIuWqsa22PtkRkgJ4
[4]: https://developers.google.com/compute/docs/gcutil/
[5]: https://cloud.google.com/console
