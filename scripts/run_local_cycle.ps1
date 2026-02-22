param(
  [int]$Generate = 5,
  [int]$Matches = 50,
  [string]$CommitMessage = "chore: local epi-ape cycle update"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir

Set-Location $rootDir

python -m backend.epi_ape.cli init
python -m backend.epi_ape.cli run-cycle --generate $Generate --matches $Matches --sync-github --commit-message $CommitMessage
