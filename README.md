# fiap-orch-sales

Orquestrador do fluxo de **venda de veículos**.  
Este microsserviço coordena chamadas para os serviços de **compradores**, **veículos** e **pagamentos**, consolidando todo o processo de compra em uma única operação.

---

## 📌 Funcionalidade

O `fiap-orch-sales` expõe um endpoint principal (`/purchase`) que:
1. Valida e resolve o comprador pelo `sub` (UUID) do Keycloak.
2. Reserva o veículo escolhido para o comprador.
3. Cria e processa o pagamento associado ao veículo.
4. Mocka os passos finais de aprovação do pagamento e venda do veículo (sem mensageria real por enquanto).
5. Retorna uma **ordem consolidada de compra** contendo IDs de comprador, veículo, pagamento e status final da transação.

---

## 🏗️ Arquitetura

O serviço segue um padrão de **arquitetura em camadas** com inspiração em **DDD e hexagonal**:

- **API Layer**: 
  - `src/api/api.py` → expõe os endpoints REST com FastAPI.
  - `src/api/auth.py` → integração com Keycloak para autenticação JWT.

- **Use Cases**: 
  - `src/usecases/purchase.py` → implementa o caso de uso de compra de veículo.

- **Adapters**:
  - `src/adapters/buyers_client.py` → integra com o `srv-buyers`.
  - `src/adapters/vehicles_client.py` → integra com o `srv-vehicles`.
  - `src/adapters/payments_client.py` → integra com o `srv-payment`.

- **Schemas (DTOs)**:
  - `src/schemas/purchase.py` → define `PurchaseIn` (entrada) e `PurchaseOut` (saída).

- **Config**:
  - `src/core/config.py` → variáveis de ambiente e URLs dos serviços dependentes.

---

## 🔐 Autenticação

- O serviço valida requisições usando **JWT emitidos pelo Keycloak**.
- O token deve ser enviado no header:
  ```
  Authorization: Bearer <access_token>
  ```

---

## 📡 Endpoints

### Compras
- `POST /purchase`
  - **Descrição**: inicia o fluxo completo de compra.
  - **Headers**: `Authorization: Bearer <token>`
  - **Body**:
    ```json
    {
      "vehicle_id": "UUID",
      "payment_method": "credit_card"
    }
    ```
  - **Resposta**:
    ```json
    {
      "order_id": "UUID",
      "vehicle_id": "UUID",
      "buyer_id": "UUID",
      "payment_id": "UUID",
      "status": "SUCCESS"
    }
    ```

---

## 🧪 O que está mockado

Como ainda não há mensageria/eventos implementados:
- O **pagamento é aprovado automaticamente** após ser criado (`PATCH /payments/{id}`).
- O **veículo é marcado como vendido automaticamente** após aprovação (`POST /vehicles/{id}/sell`).

Esses passos **seriam assíncronos** em um ambiente real, disparados por eventos de mensageria.

---

## 🚀 Próximos Passos

- [ ] Integrar mensageria (Kafka, RabbitMQ ou SQS) para eventos de **pagamento aprovado/rejeitado**.
- [ ] Tornar o fluxo resiliente com **compensações** (ex.: desfazer reserva se pagamento falhar).
- [ ] Testes de contrato e integração entre orquestrador e microsserviços.
- [ ] Observabilidade (metrics + tracing com OpenTelemetry).

---

## ⚙️ Execução local

1. Subir os microsserviços dependentes (buyers, vehicles, payments, keycloak).
2. Subir o orquestrador:
   ```bash
   docker-compose up fiap-orch-sales
   ```
---

## 📖 Stack Técnica

- **FastAPI** (Python 3.12)
- **httpx** (chamadas assíncronas aos outros microsserviços)
- **Keycloak** (autenticação/autorização via OIDC)
- **Docker Compose** (infra local)
- **Pydantic** (validação de schemas)
