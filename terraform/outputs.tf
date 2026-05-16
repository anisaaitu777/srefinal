output "application_namespace" {
  value       = kubernetes_namespace.app_ns.metadata[0].name
  description = "Имя созданного namespace для приложения"
}

output "monitoring_namespace" {
  value       = kubernetes_namespace.monitoring_ns.metadata[0].name
  description = "Имя созданного namespace для мониторинга"
}

output "helm_release_status" {
  value       = helm_release.prometheus_stack.status
  description = "Статус деплоя стека мониторинга"
}