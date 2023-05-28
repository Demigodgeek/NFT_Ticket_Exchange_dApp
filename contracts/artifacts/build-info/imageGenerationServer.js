const express = require('express');
const blockies = require('blockies');
const app = express();

app.get('/generate-image', (req, res) => {
  const { invitationId, sentence } = req.query;

  // Generate the image using blockies.js
  const image = blockies
    .create({
      seed: invitationId.toString(),
      size: 8,
      scale: 4,
      color: '#dfe',
      bgcolor: '#aabbcc',
      spotcolor: '#992233',
      spotcolor2: '#998877',
    })
    .toDataURL();

  res.send(image);
});

app.listen(3000, () => {
  console.log('Image generation server listening on port 3000!');
});