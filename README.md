## appengine-scipy-zombie-apocalypse

This sample is inspired by a [Zombie Apocalypse ODEINT demo][1] listed
in the [Scipy Cookbook][2].

## Deploying

1. Make sure that you are invited to the [VM Runtime Trusted Tester
   Program][3], and download the custom SDK.
2. Update the `application` value of the `app.yaml` file from
   `your-app-id` to the Application ID which is whitelisted for the VM
   Runtime Trusted Tester Program.
3. Run the following command:

   ```
   $ $CUSTOM_SDK_DIR/appcfg.py -R update /path/to/application
   ```

## Installing dependency

Currently, you need to install dependencies on the server manually. We
think this is bad because these dependencies will be lost upon server
restart. We're discussing how we can provide a way for users to
install dependencies upon deployments.

0. Install [gcutil][4] if you haven't.

1. Go to the [Cloud Console][5] and choose the project which is under
   the Trusted Tester Program.
2. Click Compute Engine.
3. Click the instance for the version `1` or the version you are using
   if you changed it from `1`.
4. In the instance details, scroll down to the bottom and find the
   clickable word "ssh", and click it.
5. Copy the displayed command and execute it on your command line.
6. Run the following commands:

   ```
   $ sudo apt-get update
   $ sudo apt-get install python-numpy python-scipy python-matplotlib
   ```

## Run the application

Only for the first time for one VM, you need to re-deploy the app for
recovering an import error.

```
$ $CUSTOM_SDK_DIR/appcfg.py -R update /path/to/application
```

And visit the following URL:

    http://your-app-id.appspot.com/


## Contributing changes

* See [CONTRIB.md](CONTRIB.md)

## Licensing

* See [LICENSE](LICENSE)

[1]: http://wiki.scipy.org/Cookbook/Zombie_Apocalypse_ODEINT
[2]: http://wiki.scipy.org/Cookbook/
[3]: https://docs.google.com/document/d/1VH1oVarfKILAF_TfvETtPPE3TFzIuWqsa22PtkRkgJ4
[4]: https://developers.google.com/compute/docs/gcutil/
[5]: https://cloud.google.com/console
