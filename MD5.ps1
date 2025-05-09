param(
 # The path to the file (positional parameter)
 $FilePath
)
# Get the current working directory where the script is being called from
$currentWorkingDirectory = Get-Location

# Check if the file path was provided
if (-not $FilePath) {
 Write-Error "Please provide the path to the file as an argument."
 exit 1
}
# Combine the current working directory with the provided path if it's relative
if (-not ([System.IO.Path]::IsPathRooted($FilePath))) {
 $resolvedFilePath = Join-Path -Path $currentWorkingDirectory -ChildPath $FilePath
} else {
 $resolvedFilePath = $FilePath # It's already an absolute path
}

# Check if the file exists
if (-not (Test-Path -Path $resolvedFilePath -PathType Leaf)) {
 Write-Error "File not found: '$resolvedFilePath'"
 exit 1
}

try {
 # Calculate the MD5 hash of the file
 $Hasher = [System.Security.Cryptography.MD5]::Create()
 $FileStream = [System.IO.FileStream]::new($resolvedFilePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read)
 $HashBytes = $Hasher.ComputeHash($FileStream)
 $FileStream.Close()
 $Hasher.Dispose()

 # Convert the byte array to a Base64 string
 $Base64String = [System.Convert]::ToBase64String($HashBytes)

 # Output the Base64 encoded MD5 hash
 Write-Output "MD5 Base64 for '$resolvedFilePath': $Base64String"

}
catch {
 Write-Error "An error occurred: $($_.Exception.Message)"
 exit 1
}