fetch('http://localhost:5000/api')
  .then(response => response.json())
  .then(data => console.log(data));
  fetch('/api/usuarios', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Erro:', error));
