# 1. Создаем изолированный Namespace для приложения
resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = var.app_namespace
    labels = {
      env = var.environment
    }
  }
}

# 2. Создаем изолированный Namespace для Observability стека
resource "kubernetes_namespace" "monitoring_ns" {
  metadata {
    name = var.monitoring_namespace
  }
}

# 3. Автоматически разворачиваем kube-prometheus-stack через Helm
resource "helm_release" "prometheus_stack" {
  name       = "kube-prometheus-stack"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = kubernetes_namespace.monitoring_ns.metadata[0].name
  version    = "45.7.1"

  # Активируем Grafana
  set {
    name  = "grafana.enabled"
    value = "true"
  }

  # Переводим Grafana в тип NodePort, чтобы открыть её снаружи для тестов
  set {
    name  = "grafana.service.type"
    value = "NodePort"
  }

  # Позволяем Prometheus автоматически подхватывать кастомные ServiceMonitor'ы приложения
  set {
    name  = "prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues"
    value = "false"
  }
  set {
    name  = "prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues"
    value = "false"
  }
}