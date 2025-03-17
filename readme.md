### **📘 Budget Tracker **  

## **📌 Project Summary**  
**Budget Tracker** is a cost-tracking and reporting system that extracts, processes, and loads cloud billing data from multiple providers like **AWS, Azure, GCP, and RN**. The system generates fake cost data, processes it into structured formats, and loads it into a database for further analysis.  

The project is containerized using **Docker**, making it easy to set up and run in any environment.  

---

## **🚀 How to Run the Project with Docker**  

### **1️⃣ Clone the Repository**  
```bash
git clone <your-repo-url>
cd budget_tracker
```

### **2️⃣ Build the Docker Image**  
```bash
docker compose build --no-cache
```

### **3️⃣ Start the Containers**  
```bash
docker compose up -d
```

### **4️⃣ Access the Running Container**  
```bash
docker compose exec backend bash
```

### **5️⃣ Run the Script Manually (If Needed)**  
```bash
python budget_tracker/main.py
```

---

## **📌 Project Structure**
```
budget_tracker/
│── aws/               # AWS data processing
│── azure/             # Azure data processing
│── gcp/               # GCP data processing
│── rn/                # RN data processing
│── lib/               # Helper utilities (DB, Faker)
│── main.py            # Main script to run the project
│── Dockerfile         # Docker configuration
│── docker-compose.yml # Docker Compose setup
│── requirements.txt   # Python dependencies
```

---

## **📌 Useful Commands**
🔹 **Stop Containers:**  
```bash
docker compose down
```

🔹 **Check Logs:**  
```bash
docker compose logs -f
```

🔹 **Rebuild After Code Changes:**  
```bash
docker compose up --build -d
```

---
