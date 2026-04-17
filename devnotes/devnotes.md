cd /c/Code && cp -r cw-apworld content_warning && 7z a -tzip content_warning.apworld ./content_warning/ -xr\!.git -xr\!Sample -xr\!devnotes.md* && rm -rf content_warning

New command to make apworld file

set +H && cp -r cw-apworld/ap_world content_warning && 7z a -tzip content_warning.apworld content_warning -xr\!.git -xr\!Sample -xr\!devnotes.md* && rm -rf content_warning

set +H && cp -r ap_world content_warning && 7z a -tzip content_warning.apworld content_warning -xr\!.git -xr\!.Sample -xr\!devnotes.md* && rm -rf content_warning