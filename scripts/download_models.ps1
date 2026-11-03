# =====================================================================
# Script de Download de Modelos para ComfyUI (Otimizados para RTX 2060 6GB)
# =====================================================================

param (
    [string]$Option = ""
)

$BASE_DIR = "$PSScriptRoot\..\storage\comfyui\models"

function Download-FileWithProgress {
    param (
        [string]$Url,
        [string]$DestinationPath,
        [string]$Description
    )

    $parentDir = Split-Path -Parent $DestinationPath
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }

    if (Test-Path $DestinationPath) {
        Write-Host "[OK] Ja existe: $Description" -ForegroundColor Green
        return
    }

    Write-Host "[BAIXANDO] $Description..." -ForegroundColor Cyan
    Write-Host "URL: $Url" -ForegroundColor DarkGray
    Write-Host "Destino: $DestinationPath" -ForegroundColor DarkGray

    try {
        # Usa curl.exe se disponivel (mais rapido e estavel no Windows)
        if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
            & curl.exe -L --progress-bar -o "$DestinationPath" "$Url"
        } else {
            Start-BitsTransfer -Source $Url -Destination $DestinationPath -Description $Description
        }
        Write-Host "[CONCLUIDO] $Description baixado com sucesso!`n" -ForegroundColor Green
    }
    catch {
        Write-Host "[ERRO] Falha ao baixar $Description : $_" -ForegroundColor Red
    }
}

Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host "   Downloader de Modelos de IA de Video para ComfyUI      " -ForegroundColor Magenta
Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host "Modelos otimizados para funcionar com 6GB VRAM (Offload para RAM)`n"

if (-not $Option) {
    Write-Host "Escolha uma opcao:"
    Write-Host "1 - AnimateDiff Pack (DreamShaper 8 SD1.5 + Motion Module v2) [~3.9 GB]" -ForegroundColor Yellow
    Write-Host "2 - epiCPhotoGasm Checkpoint (Ultra Realismo Humano Fotográfico) [~2.1 GB]" -ForegroundColor Green
    Write-Host "3 - LTX-Video 0.9.1 (Lightricks Text-to-Video 2B) [~4.8 GB]" -ForegroundColor Yellow
    Write-Host "4 - Exibir links para Wan 2.1 (1.3B GGUF)" -ForegroundColor Yellow
    Write-Host "0 - Sair"
    $Option = Read-Host "Digite o numero da opcao"
}

switch ($Option) {
    "1" {
        Write-Host "`nIniciando download do pacote AnimateDiff..." -ForegroundColor Cyan
        
        # 1. Checkpoint SD1.5 (DreamShaper 8)
        $checkpointDest = "$BASE_DIR\checkpoints\DreamShaper_8_pruned.safetensors"
        $checkpointUrl = "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_8_pruned.safetensors"
        Download-FileWithProgress -Url $checkpointUrl -DestinationPath $checkpointDest -Description "Checkpoint DreamShaper 8 (SD 1.5)"

        # 2. Motion Module AnimateDiff v2
        $motionDest = "$BASE_DIR\animatediff_models\mm_sd_v15_v2.ckpt"
        $motionUrl = "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt"
        Download-FileWithProgress -Url $motionUrl -DestinationPath $motionDest -Description "Motion Module AnimateDiff v2 (mm_sd_v15_v2.ckpt)"
        
        Write-Host "Pronto! O pacote AnimateDiff esta pronto para uso no ComfyUI." -ForegroundColor Green
    }
    "2" {
        Write-Host "`nIniciando download do epiCPhotoGasm (Hiper-realismo de Pessoas)..." -ForegroundColor Cyan
        $epicDest = "$BASE_DIR\checkpoints\epicphotogasm_v1.safetensors"
        $epicUrl = "https://huggingface.co/Yntec/epiCPhotoGasm/resolve/main/epicphotogasm_v1.safetensors"
        Download-FileWithProgress -Url $epicUrl -DestinationPath $epicDest -Description "Checkpoint epiCPhotoGasm (SD 1.5 Fotográfico)"
    }
    "3" {
        Write-Host "`nIniciando download do LTX-Video..." -ForegroundColor Cyan
        $ltxDest = "$BASE_DIR\checkpoints\ltx-video-2b-v0.9.1.safetensors"
        $ltxUrl = "https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltx-video-2b-v0.9.1.safetensors"
        Download-FileWithProgress -Url $ltxUrl -DestinationPath $ltxDest -Description "LTX-Video 2B v0.9.1 Checkpoint"
    }
    "4" {
        Write-Host "`nO Wan 2.1 (1.3B) possui multiplos componentes quantizados (GGUF):" -ForegroundColor Cyan
        Write-Host "1. Modelo Diffusion (GGUF Q4_K_M): https://huggingface.co/city96/Wan2.1-T2V-1.3B-gguf" -ForegroundColor White
        Write-Host "   Salvar em: storage/comfyui/models/diffusion_models/" -ForegroundColor DarkGray
        Write-Host "2. Text Encoder (umt5_xxl FP8): https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged" -ForegroundColor White
        Write-Host "   Salvar em: storage/comfyui/models/text_encoders/" -ForegroundColor DarkGray
        Write-Host "3. VAE (wan_2.1_vae.safetensors): https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged" -ForegroundColor White
        Write-Host "   Salvar em: storage/comfyui/models/vae/" -ForegroundColor DarkGray
    }
    default {
        Write-Host "Operacao cancelada ou opcao invalida." -ForegroundColor Yellow
    }
}

