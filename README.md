# EFF packaging
Purpose:
Provide a tool to process the amended EFF package from a well packaged EFF with the recalculated MD5 Base64 hash for eff.lst file

Use case:
To generate a training EFF package from a normal flight

Design logic:
1. The .eff file is a zipped file containing a .lst and .dat files, .dat file is the zipped filed containing all the package files.
2. All the files containing in the packages except the .lst file need to have a MD5 Base64 hash code listed in the .lst file.
3. The tool will unzip the .eff and then unzip the .dat file to a subfolder name dat.
4. recalculate the MD5 BASE64 hash code for all the files in the .dat folder and amend the .lst files for those files's hash code.
5. zip the files in the dat folder and rename the extension to .dat
6. recalculate the .dat file MD5 Base64 hash and amend the eff.lst file accordinatly.
7. zip the eff.lst and .dat file to a .eff file.
