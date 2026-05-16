variable "kube_config_path" {
  type        = string
  default     = "~/.kube/config"
  description = "Путь к вашему конфигурационному файлу kubeconfig"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Окружение для деплоя (production/staging)"
}

variable "app_namespace" {
  type        = string
  default     = "srefinal-prod"
  description = "Пространство имен Kubernetes для нашего Node.js приложения"
}

variable "monitoring_namespace" {
  type        = string
  default     = "monitoring"
  description = "Пространство имен Kubernetes для Prometheus и Grafana"
}