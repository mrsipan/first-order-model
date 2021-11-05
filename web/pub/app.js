function showImage (fileInput) {
  const files = fileInput.files
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    const imageType = /image.*/
    if (!file.type.match(imageType)) {
      continue
    }
    const img = document.getElementById('thumbnail')
    img.file = file
    const reader = new FileReader()
    reader.onload = (function (aImg) {
      return function (e) {
        aImg.src = e.target.result
      }
    })(img)
    reader.readAsDataURL(file)

    // Send to server
    const formData = new FormData()
    formData.append('test-image', files[0])

    fetch('/do', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(rv => {
        console.log(rv.path)
      })
      .catch(error => {
        console.log('Error')
      })

    const video = document.getElementById('video')
    video.src = rv.path
  }
}
