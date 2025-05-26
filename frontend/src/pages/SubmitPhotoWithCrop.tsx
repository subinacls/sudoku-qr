
import { useState } from 'react'
import Cropper from 'react-easy-crop'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { backendURL } from '../config'

function getCroppedImg(src: string, area: any): Promise<Blob> {
  return new Promise(async (resolve, reject) => {
    const image = new Image()
    image.src = src
    image.onload = () => {
      const canvas = document.createElement('canvas')
      canvas.width = area.width
      canvas.height = area.height
      const ctx = canvas.getContext('2d')!
      ctx.drawImage(
        image,
        area.x,
        area.y,
        area.width,
        area.height,
        0,
        0,
        area.width,
        area.height
      )
      canvas.toBlob(blob => {
        if (blob) resolve(blob)
        else reject(new Error('Crop failed'))
      }, 'image/png')
    }
    image.onerror = reject
  })
}

export default function SubmitPhotoWithCrop() {
  const { qrToken } = useParams()
  const [imageSrc, setImageSrc] = useState<string | null>(null)
  const [crop, setCrop] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)
  const [area, setArea] = useState<any>(null)

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => setImageSrc(reader.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async () => {
    if (!imageSrc || !area) return
    const blob = await getCroppedImg(imageSrc, area)
    const form = new FormData()
    form.append('file', blob, 'sudoku.png')
    await axios.post(`${backendURL}/submit/photo/${qrToken}`, form)
    alert('Submitted!')
  }

  return (
    <div className="p-4 flex flex-col items-center">
      <input type="file" accept="image/*" onChange={onFileChange}/>
      {imageSrc && (
        <div className="relative w-80 h-80 mt-4">
          <Cropper
            image={imageSrc}
            crop={crop}
            zoom={zoom}
            aspect={1}
            onCropChange={setCrop}
            onZoomChange={setZoom}
            onCropComplete={(_, areaPixels) => setArea(areaPixels)}
          />
        </div>
      )}
      <button className="bg-purple-500 text-white px-4 py-2 rounded mt-4" onClick={handleSubmit}>Submit</button>
    </div>
  );
}
