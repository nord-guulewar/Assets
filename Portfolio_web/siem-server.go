package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
	"github.com/rs/cors"
)

type Event struct {
	ID          int    `json:"id"`
	Timestamp   string `json:"timestamp"`
	Source      string `json:"source"`
	EventType   string `json:"event_type"`
	Severity    string `json:"severity"`
	Message     string `json:"message"`
	SourceIP    string `json:"source_ip"`
	UserAgent   string `json:"user_agent,omitempty"`
}

type Alert struct {
	ID        int    `json:"id"`
	Timestamp string `json:"timestamp"`
	Title     string `json:"title"`
	Message   string `json:"message"`
	Severity  string `json:"severity"`
	Source    string `json:"source"`
	Status    string `json:"status"`
}

type Metrics struct {
	TotalEvents    int     `json:"total_events"`
	ActiveAlerts   int     `json:"active_alerts"`
	ThreatsBlocked int     `json:"threats_blocked"`
	SystemUptime   float64 `json:"system_uptime"`
	EventsPerSec   int     `json:"events_per_second"`
}

type SIEMServer struct {
	events  []Event
	alerts  []Alert
	clients map[*websocket.Conn]bool
}

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow connections from any origin
	},
}

func NewSIEMServer() *SIEMServer {
	return &SIEMServer{
		events:  make([]Event, 0),
		alerts:  make([]Alert, 0),
		clients: make(map[*websocket.Conn]bool),
	}
}

func (s *SIEMServer) generateEvent() Event {
	eventTypes := []string{"LOGIN_SUCCESS", "LOGIN_FAILED", "FILE_ACCESS", "NETWORK_CONNECTION", "SYSTEM_ALERT"}
	severities := []string{"INFO", "WARN", "ERROR"}
	sources := []string{"web-server", "database", "firewall", "endpoint", "api-gateway"}

	eventType := eventTypes[rand.Intn(len(eventTypes))]
	severity := severities[rand.Intn(len(severities))]
	source := sources[rand.Intn(len(sources))]

	message := fmt.Sprintf("%s event from %s", eventType, source)
	sourceIP := fmt.Sprintf("192.168.%d.%d", rand.Intn(255), rand.Intn(255))

	return Event{
		ID:        len(s.events) + 1,
		Timestamp: time.Now().Format(time.RFC3339),
		Source:    source,
		EventType: eventType,
		Severity:  severity,
		Message:   message,
		SourceIP:  sourceIP,
	}
}

func (s *SIEMServer) generateAlert() Alert {
	alertTitles := []string{
		"Brute Force Attack Detected",
		"Suspicious File Access",
		"Unusual Network Traffic",
		"Privilege Escalation Attempt",
		"Malware Signature Detected",
	}
	severities := []string{"critical", "high", "medium", "low"}
	sources := []string{"IDS", "Endpoint Protection", "Firewall", "SIEM Correlation"}

	title := alertTitles[rand.Intn(len(alertTitles))]
	severity := severities[rand.Intn(len(severities))]
	source := sources[rand.Intn(len(sources))]

	message := fmt.Sprintf("Alert triggered by %s detection engine", source)

	return Alert{
		ID:        len(s.alerts) + 1,
		Timestamp: time.Now().Format(time.RFC3339),
		Title:     title,
		Message:   message,
		Severity:  severity,
		Source:    source,
		Status:    "active",
	}
}

func (s *SIEMServer) getMetrics() Metrics {
	totalEvents := len(s.events)
	activeAlerts := 0
	for _, alert := range s.alerts {
		if alert.Status == "active" {
			activeAlerts++
		}
	}

	return Metrics{
		TotalEvents:    totalEvents,
		ActiveAlerts:   activeAlerts,
		ThreatsBlocked: rand.Intn(50) + 10,
		SystemUptime:   99.5 + rand.Float64()*0.4,
		EventsPerSec:   rand.Intn(100) + 50,
	}
}

// HTTP Handlers
func (s *SIEMServer) handleMetrics(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	metrics := s.getMetrics()
	json.NewEncoder(w).Encode(metrics)
}

func (s *SIEMServer) handleEvents(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Return last 50 events
	start := len(s.events) - 50
	if start < 0 {
		start = 0
	}

	recentEvents := s.events[start:]
	json.NewEncoder(w).Encode(recentEvents)
}

func (s *SIEMServer) handleAlerts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Return active alerts
	activeAlerts := make([]Alert, 0)
	for _, alert := range s.alerts {
		if alert.Status == "active" {
			activeAlerts = append(activeAlerts, alert)
		}
	}

	json.NewEncoder(w).Encode(activeAlerts)
}

func (s *SIEMServer) handleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket upgrade failed:", err)
		return
	}
	defer conn.Close()

	s.clients[conn] = true
	defer delete(s.clients, conn)

	// Send initial data
	metrics := s.getMetrics()
	conn.WriteJSON(map[string]interface{}{
		"type":    "metrics",
		"data":    metrics,
	})

	// Keep connection alive and send periodic updates
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// Generate new event and alert
			event := s.generateEvent()
			alert := s.generateAlert()

			s.events = append(s.events, event)
			s.alerts = append(s.alerts, alert)

			// Keep only last 1000 events and 100 alerts
			if len(s.events) > 1000 {
				s.events = s.events[1:]
			}
			if len(s.alerts) > 100 {
				s.alerts = s.alerts[1:]
			}

			// Send updates to client
			metrics := s.getMetrics()
			conn.WriteJSON(map[string]interface{}{
				"type":    "metrics_update",
				"data":    metrics,
			})

			conn.WriteJSON(map[string]interface{}{
				"type":    "new_event",
				"data":    event,
			})

			conn.WriteJSON(map[string]interface{}{
				"type":    "new_alert",
				"data":    alert,
			})
		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	server := NewSIEMServer()

	// Initialize with some sample data
	for i := 0; i < 100; i++ {
		server.events = append(server.events, server.generateEvent())
	}
	for i := 0; i < 10; i++ {
		server.alerts = append(server.alerts, server.generateAlert())
	}

	r := mux.NewRouter()

	// API routes
	r.HandleFunc("/api/metrics", server.handleMetrics).Methods("GET")
	r.HandleFunc("/api/events", server.handleEvents).Methods("GET")
	r.HandleFunc("/api/alerts", server.handleAlerts).Methods("GET")
	r.HandleFunc("/ws", server.handleWebSocket)

	// CORS middleware
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"*"},
		AllowCredentials: true,
	})

	handler := c.Handler(r)

	fmt.Println("SIEM Dashboard API Server starting on :8080")
	fmt.Println("Available endpoints:")
	fmt.Println("  GET  /api/metrics  - Get current metrics")
	fmt.Println("  GET  /api/events   - Get recent events")
	fmt.Println("  GET  /api/alerts   - Get active alerts")
	fmt.Println("  WS   /ws           - WebSocket for real-time updates")

	log.Fatal(http.ListenAndServe(":8080", handler))
}