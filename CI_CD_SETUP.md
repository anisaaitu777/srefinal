# CI/CD GitHub Actions Setup - Инструкция

## Шаг 1: Настройка GitHub Secrets

Перейдите в **Settings** вашего репо → **Secrets and variables** → **Actions** и добавьте следующие секреты:

### 1.1 Docker Hub учётные данные

#### `DOCKERHUB_USERNAME`
- Ваше имя пользователя на Docker Hub (например: `your_username`)

#### `DOCKERHUB_TOKEN`
- Personal Access Token с Docker Hub
- Как получить:
  1. Войдите в Docker Hub (https://hub.docker.com)
  2. Нажмите на аватар → **Account Settings**
  3. Слева выберите **Security**
  4. Нажмите **New Access Token**
  5. Дайте ему имя (например: `github-actions`)
  6. Скопируйте токен и добавьте в GitHub Secrets

### 1.2 Kubernetes конфигурация

#### `KUBE_CONFIG`
Это **самое важное** - ваш kubeconfig файл в base64 кодировке.

**Как получить kubeconfig:**

**Если вы используете локальный кластер (Docker Desktop, Minikube):**
```bash
# Для Docker Desktop
cat ~/.kube/config | base64 -w 0 > kubeconfig_base64.txt

# Для Minikube
minikube kubectl config view | base64 -w 0 > kubeconfig_base64.txt
```

**Если вы используете облачный кластер:**
- **AWS (EKS)**: `aws eks update-kubeconfig --name your-cluster-name --region your-region`
- **GCP (GKE)**: `gcloud container clusters get-credentials cluster-name --zone zone`
- **Azure (AKS)**: `az aks get-credentials --resource-group rg-name --name cluster-name`

Затем закодируйте в base64:
```bash
cat ~/.kube/config | base64 -w 0 > kubeconfig_base64.txt
```

**На Windows (PowerShell):**
```powershell
$content = Get-Content $env:USERPROFILE\.kube\config -Raw
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content)) | Set-Content kubeconfig_base64.txt
```

Скопируйте содержимое `kubeconfig_base64.txt` в GitHub Secret `KUBE_CONFIG`.

---

## Шаг 2: Проверка Kubernetes namespace

Убедитесь, что namespace `srefinal-prod` существует:

```bash
kubectl create namespace srefinal-prod
```

---

## Шаг 3: Проверка прав доступа

Убедитесь, что ваш kubeconfig пользователь имеет права на:
- Создание/обновление deployments
- Создание/обновление services
- Просмотр статуса rollouts

Проверить текущие права:
```bash
kubectl auth can-i create deployments --namespace srefinal-prod
kubectl auth can-i create services --namespace srefinal-prod
```

---

## Шаг 4: Тестирование

1. Сделайте commit в `main` ветку:
```bash
git add .
git commit -m "Enable CI/CD pipeline"
git push origin main
```

2. Перейдите в **Actions** в вашем GitHub репо
3. Дождитесь завершения workflow
4. Проверьте логи обоих jobs: `build-and-push` и `deploy-to-cluster`

---

## Отладка проблем

### ❌ Error: Docker login failed
- Проверьте `DOCKERHUB_USERNAME` и `DOCKERHUB_TOKEN`
- Убедитесь, что токен не истёк

### ❌ Error: Unable to connect to cluster
- Проверьте что `KUBE_CONFIG` корректно закодирован в base64
- Убедитесь, что kubeconfig файл валидный: `kubectl config view` 

### ❌ Error: Deployment rollout failed
- Проверьте образ в Docker Hub загружен правильно
- Убедитесь, что есть достаточно ресурсов в кластере
- Посмотрите логи пода: `kubectl describe pod -n srefinal-prod`

### ❌ Error: Permission denied
- Убедитесь, что пользователь в kubeconfig имеет права RBAC
- Попробуйте: `kubectl get deployments -n srefinal-prod`

---

## Что происходит при каждом push в main?

1. ✅ Checkout кода
2. ✅ Сборка Docker образа
3. ✅ Push образа в Docker Hub с двумя тегами:
   - `latest` - для последней версии
   - `latest-<commit-sha>` - для версионирования
4. ✅ Deploy в Kubernetes:
   - Обновление image в deployment
   - Применение manifests
   - Проверка statuses подов
   - Вывод информации о развёрнутых ресурсах

---

## Полезные команды для отладки

```bash
# Проверить статус deployment
kubectl get deployment srefinal-app -n srefinal-prod

# Посмотреть логи подов
kubectl logs deployment/srefinal-app -n srefinal-prod

# Описание deployment
kubectl describe deployment srefinal-app -n srefinal-prod

# Проверить сервис
kubectl get service srefinal-service -n srefinal-prod

# Тест подключения к приложению (если используется NodePort)
curl http://localhost:30080
```

---

## Дополнительно: GitHub Actions Secrets

Репо Secrets находятся по адресу:
```
https://github.com/YOUR_USERNAME/srefinal/settings/secrets/actions
```

Убедитесь что добавили все 3 секрета:
- ✅ `DOCKERHUB_USERNAME`
- ✅ `DOCKERHUB_TOKEN`  
- ✅ `KUBE_CONFIG`
