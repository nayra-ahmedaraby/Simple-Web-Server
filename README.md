# Simple Web Server

A lightweight web server built using Python's socket programming and threading. It handles multiple client requests, serves static HTML content, and includes a dynamic status endpoint showing server uptime.

---

## 🔧 Features

- Serves HTML pages over HTTP  
- Handles multiple requests using threading  
- Dynamic `/status` endpoint with live server uptime  
- Simple routing and error handling (404)  
- Configurable via `config.json`

---

## 🛠️ Technologies Used

- Python 3  
- Sockets  
- Threading  
- HTML  
- JSON

---

## 📂 Project Structure

```
├── server.py              # Main server logic
├── config.json            # Configurable server settings
├── HelloWorld.html        # Default homepage
├── status.html            # Dynamic uptime page
├── 404.html               # Error page for invalid routes
├── README.md              # Project documentation
```

---

## ⚙️ How to Run

1. Make sure you have **Python 3.x** installed.  
2. (Optional) Modify `config.json` to change port or default page.  
3. Run the server:
   ```bash
   py server.py
   ```
4. Open your browser and go to:
   ```
   http://localhost:6789/
   ```

---

## 🌐 Routes

| Route            | Description                  |
|------------------|------------------------------|
| `/`              | Loads the default homepage   |
| `/status`        | Shows server uptime          |
| `/invalid`       | Triggers custom 404 page     |
| `/yourfile.html` | Loads any available HTML file|

---

## 📈 Impact

This project provides a clear understanding of how web servers work at a low level, offering hands-on experience with:
- HTTP requests/responses  
- Socket communication  
- Multi-threaded request handling

---

## 📎 License

This project is for educational purposes and open for improvement or extension.
