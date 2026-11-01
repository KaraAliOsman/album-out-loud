# Reads the English sample letter aloud with the offline Windows speech engine
# and saves it as a WAV file. It stops after the closing line, where the letter
# tells the listener they can stop; the file list for the helper is not read.
param(
  [string]$Letter = "$PSScriptRoot\..\assets\sample_letter.txt",
  [string]$Out = "$PSScriptRoot\..\assets\sample_letter.wav",
  [string]$Voice = 'Microsoft Zira Desktop'
)
Add-Type -AssemblyName System.Speech
$lines = [System.IO.File]::ReadAllLines((Resolve-Path $Letter), [System.Text.Encoding]::UTF8)
$pb = New-Object System.Speech.Synthesis.PromptBuilder
foreach ($line in $lines) {
  if ($line -like 'For the helper: photo files*') { break }
  if ($line.Trim() -eq '') { $pb.AppendBreak([TimeSpan]::FromMilliseconds(900)); continue }
  $pb.AppendText($line)
  $pb.AppendBreak([TimeSpan]::FromMilliseconds(350))
}
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice($Voice)
$s.Rate = 0
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(22050, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
$s.SetOutputToWaveFile([System.IO.Path]::GetFullPath($Out), $fmt)
$s.Speak($pb)
$s.SetOutputToNull()
$s.Dispose()
Write-Output ("Saved " + [System.IO.Path]::GetFullPath($Out))
