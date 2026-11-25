# Perfil, selos e conta - backend - Implementation Plan

> Plan produced by Termite; tasks are executed by step-03 of the termite skill.

**Goal:** Entregar no backend `medsafari` o módulo 02: perfil acadêmico, verificação, selos, privacidade de exibição, desativação/exclusão, exportação de dados e a API da fila manual da equipe.

**Architecture:** Hexagonal `domain <- application <- (adapters-postgres, adapters-http) <- bootstrap`, com seis módulos novos (`profile`, `verification`, `badges`, `privacy`, `account`, `notifications`) no layout `modules/<modulo>/<kind>/<name>.<kind>.rs` já usado por `auth`. Camada por camada, teste primeiro; migrações cedo para destravar os adaptadores.

**Tech Stack:** Rust 2024, Axum 0.8, sqlx 0.9 (`sqlx::query` sem macros), utoipa 6, mockall 0.15, testcontainers (Postgres), cargo-nextest.

**Spec:** `artifacts/active/user-profile-account/backend/delivery/02-tech-spec.md` (histórias em `01-functional-stories.md`).

## Global Constraints

- Branch `feat/user-profile-account-backend` em `repos/medsafari`; todos os caminhos abaixo são relativos a `backend/` nesse repo.
- Um commit Conventional por tarefa, com `LEFTHOOK=0`; nunca commitar com teste vermelho. Hooks rodam no VERIFY.
- Layout: um item por arquivo `<name>.<kind>.rs`, testes em `__tests__/<name>.<kind>.test.rs` ligados por `#[cfg(test)] #[path = "__tests__/..."] mod tests;`; `mod.rs` declara com `#[path]` e reexporta; `lib.rs` só tem `pub mod`.
- Testes nomeados `ac_<nn>_br_<nn>_<comportamento>`; teste unitário não toca rede, disco, relógio nem banco.
- Sem `unwrap`/`expect` fora de testes e `bootstrap`; erros com `thiserror` por camada; comentários só com o porquê, sem ids de BR/AC.
- Domínio sem dependência de framework ou runtime assíncrono; `sqlx` só em `adapters-postgres`.
- Migrações `000N_<nome>.sql` sem `.down.sql`, `timestamptz`, `uuid`, tabelas no plural, FKs `<singular>_id`, índices `idx_<tabela>_<colunas>`; integração com testcontainers em `crates/adapters-postgres/tests/`.
- Valores da spec: nome ≤ 120, histórico ≤ 500, Lattes só `lattes.cnpq.br`, comprovante PDF/JPG/PNG ≤ 5 MB, código institucional de 6 dígitos com 15 min e 5 tentativas, comprovante apagado 90 dias após a decisão, carência de exclusão 30 dias, link de exportação 7 dias e 1 pedido por 24 h, aviso do selo de Estudante 30 dias antes, atraso da fila 7 dias úteis, declaração de residência ≤ 90 dias.
- Comandos: `U` = `cargo nextest run --workspace --profile unit`; `I` = `DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run --workspace --profile integration` (Podman). Rodar de `repos/medsafari/backend`.
- Mudança no OpenAPI é mudança de API: anotar para o frontend regenerar o cliente.
- Comparação de nomes usa tabela própria de remoção de acentos do português (sem dependência nova); a decisão final continua da curadoria.

## Review Focus

- Upload com extensão `.pdf` mas conteúdo de outro tipo, ou corpo acima de 5 MB: recusado (Task 11 e 24).
- Duas contas enviando o mesmo CRM ao mesmo tempo: só uma fica verificada (Task 20).
- Exclusão executada duas vezes ou com arquivo já removido: idempotente, sem erro (Task 17 e 21).
- Conta desativada tentando usar rotas de conta ativa: 403, mas pode consultar a sessão, sair e reativar (Task 8 e 26).
- Link de exportação aberto por outra conta, sem sessão ou expirado: negado (Task 17 e 26).
- Troca para modo público sem aceite da versão vigente do termo: recusada (Task 13).
- Recusa ou revogação sem motivo: recusada (Task 10 e 25).

---

## Phase A - Domain

### Task 1: Domain account
- layer: domain
- repo: medsafari
- depends_on: []
- covers: AC-53, AC-55, AC-57, AC-58, BR-35, BR-36, BR-37
- test_scope: unit
- files: `crates/domain/src/modules/account/{mod.rs,value_objects/{mod.rs,account_status.value_object.rs},errors/{mod.rs,account.error.rs}}` + `value_objects/__tests__/account_status.value_object.test.rs`; registrar `account` em `modules/mod.rs`
- verify: `U`
- commit: `feat(domain): add account status and transitions`
- Interfaces produces: `enum AccountStatus { Ativa, Desativada, ExclusaoAgendada, Suspensa }` com `parse(&str)->Result<Self,AccountError>`, `as_str(&self)->&'static str`, `deactivate(self)`, `schedule_deletion(self)`, `reactivate(self)` (Desativada ou ExclusaoAgendada → Ativa) e `suspend(self)`, todos `Result<AccountStatus,AccountError>`; `AccountError::{InvalidTransition{from:AccountStatus,to:AccountStatus}, UnknownStatus(String)}`.
- [x] Teste: `ac_53_br_35_active_account_can_be_deactivated`, `ac_55_br_36_deactivated_account_reactivates`, `ac_58_br_37_scheduled_deletion_reactivates`, `ac_57_br_37_only_active_or_deactivated_can_schedule_deletion`, `br_35_suspended_cannot_reactivate`.
- [x] Ver falhar, implementar o mínimo, ver passar, commitar.
- commit: `5e23292`

### Task 2: Domain profile
- layer: domain
- repo: medsafari
- depends_on: [1]
- covers: AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08, AC-09, BR-01, BR-02, BR-03, BR-04, BR-05, BR-06
- test_scope: unit
- files: `crates/domain/src/modules/profile/{mod.rs,value_objects/{full_name,bio,lattes_url,situation,academic_year,crm_number,brazilian_uf,institution_text,program_status}.value_object.rs,entities/{profile,crm_registration,residency,postgraduate}.entity.rs,errors/profile.error.rs}` + um teste por arquivo em `__tests__/`
- verify: `U`
- commit: `feat(domain): add profile value objects and entities`
- Interfaces produces: `FullName::parse(&str)` (trim, 1..=120 caracteres), `Bio::parse` (≤ 500, sem caracteres de controle exceto quebra de linha), `LattesUrl::parse` (https e host `lattes.cnpq.br`), `Situation::{Estudante,Medico,Residente,Especialista}` com `parse/as_str`, `AcademicYear::parse(i32)` (1900..=2100), `CrmNumber::parse` (só dígitos, 1..=10), `BrazilianUf::parse` (27 UFs), `InstitutionText::parse` (≤ 200), `ProgramStatus::{EmCurso,Concluida}`; `enum UniversityRef { Listed(Uuid), Foreign(InstitutionText) }`; `Profile { full_name: Option<FullName>, situation: Option<Situation>, preparing_residency: bool, university: Option<UniversityRef>, admission_year: Option<AcademicYear>, graduation_year: Option<AcademicYear>, bio: Option<Bio>, lattes: Option<LattesUrl> }` com `is_complete(&self)->bool` (nome, situação e universidade; médico também ano de conclusão); `CrmRegistration { id: Uuid, number: CrmNumber, uf: BrazilianUf }`, `Residency`, `Postgraduate` (campos das seções 4.5 e 4.6; `Postgraduate::kind: PostgraduateKind::{Mestrado,Doutorado}`); todos erros em `ProfileError`.
- [x] Testes: `ac_06_br_04_rejects_name_over_120` e `bio_over_500`, `ac_07_br_04_rejects_non_lattes_host`, `ac_04_br_03_rejects_unknown_situation`, `ac_02_br_02_student_with_name_situation_university_is_complete`, `ac_03_br_02_doctor_without_graduation_year_is_incomplete`, `ac_08_br_05_foreign_university_is_accepted`, `ac_05_br_03_preparing_residency_does_not_change_completeness`, `ac_09_br_06_profile_allows_many_crm_entries`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `05cd76c`

### Task 3: Domain verification
- layer: domain
- repo: medsafari
- depends_on: [2]
- covers: AC-10, AC-11, AC-12, AC-14, AC-16, AC-20, AC-21, AC-23, AC-25, AC-27, AC-28, AC-31, AC-32, AC-34, AC-36, AC-38, BR-07, BR-11, BR-12, BR-14, BR-16, BR-18, BR-20, BR-21, BR-22, BR-23, BR-26
- test_scope: unit
- files: `crates/domain/src/modules/verification/{mod.rs,value_objects/{verification_status,verification_item_type,verification_method,rejection_reason,evidence_file,observed_crm_status,person_name_match}.value_object.rs,entities/{verification,institutional_email_challenge}.entity.rs,errors/verification.error.rs}` + testes em `__tests__/`
- verify: `U`
- commit: `feat(domain): add verification rules`
- Interfaces produces:
  - `VerificationStatus::{NaoEnviado,Pendente,Aprovado,Recusado,Revogado}`; `VerificationItemType::{Matricula,Crm,Especialista,Residencia,Pos}`; `VerificationMethod::{CarteiraCrm,EmailInstitucional,Comprovante}`; `RejectionReason::{Ilegivel,DocumentoVencido,NomeDiferente,DocumentoNaoAceito,Outro}`.
  - `EvidenceFile::validate(bytes:&[u8], declared_content_type:&str)->Result<EvidenceFile,VerificationError>` (PDF, JPG ou PNG por assinatura dos bytes, ≤ 5 MB; o tipo declarado é conferido contra a assinatura); `EvidenceFile::{content_type(),len()}`.
  - `ObservedCrmStatus::{Ativa,Outra(String)}` com `grants_badge()->bool`; `PersonNameMatch::matches(a:&str,b:&str)->bool` (sem acentos e maiúsculas, espaços colapsados).
  - `Verification` com `approve(self, decided_by:Uuid, at:OffsetDateTime)`, `reject(self, reason:RejectionReason, decided_by, at)`, `revoke(self, reason:String, at)`, todos `Result<Verification,VerificationError>`; recusa e revogação sem motivo (texto vazio) falham; `is_overdue(&self, now:OffsetDateTime)->bool` (7 dias úteis, sábado e domingo não contam); declaração de residência com `issued_at` > 90 dias é recusável via `Verification::check_residency_declaration_age`.
  - `InstitutionalEmailChallenge` com `attempt(&mut self, code_hash_matches:bool, now)->ChallengeOutcome::{Confirmed,Wrong{remaining:u8},Expired,Exhausted}` (15 min, 5 tentativas, uso único).
- [x] Testes (um por linha): `ac_28_br_22_rejects_docx_and_over_5mb`, `ac_28_br_22_rejects_pdf_extension_with_png_bytes`, `ac_21_br_16_name_match_ignores_accents_and_case`, `ac_20_br_16_different_names_do_not_match`, `ac_16_br_14_non_active_crm_never_grants_badge`, `ac_36_br_23_reject_requires_reason`, `ac_43_br_27_revoke_requires_reason`, `ac_32_br_07_new_item_is_not_sent`, `ac_14_br_07_submitted_is_pending`, `ac_38_br_26_pending_over_seven_business_days_is_overdue`, `ac_25_br_20_declaration_older_than_90_days_is_expired`, `ac_27_br_21_in_progress_postgraduate_does_not_qualify`, `ac_10_br_12_code_confirms_once`, `ac_11_br_12_challenge_locks_after_five_wrong_codes`, `ac_34_br_24_decision_records_who_and_when`, `ac_23_br_18_crm_check_keeps_only_status_and_specialties`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `33bb01f`

### Task 4: Domain badges, privacy e notifications
- layer: domain
- repo: medsafari
- depends_on: [2, 3]
- covers: AC-39, AC-40, AC-41, AC-42, AC-45, AC-47, AC-48, AC-49, AC-51, AC-52, AC-67, AC-68, AC-69, BR-08, BR-09, BR-10, BR-13, BR-29, BR-30, BR-31, BR-32, BR-34, BR-42
- test_scope: unit
- files: `crates/domain/src/modules/badges/{mod.rs,value_objects/badge_type.value_object.rs,entities/badge.entity.rs}`, `modules/privacy/{mod.rs,value_objects/display_mode.value_object.rs,entities/author_display.entity.rs}`, `modules/notifications/{mod.rs,value_objects/notification_kind.value_object.rs}` + testes
- verify: `U`
- commit: `feat(domain): add badges, author display and notification kinds`
- Interfaces produces:
  - `BadgeType::{Estudante,Medico,Residente,Especialista,Mestre,Doutor}` com `priority()` e `primary_badge(active:&[Badge])->Option<&Badge>` (Doutor, Mestre, Especialista, Residente, Médico, Estudante); `Badge { id:Uuid, kind:BadgeType, detail:Option<String>, verification_id:Uuid, valid_until:Option<OffsetDateTime>, revoked_at:Option<OffsetDateTime> }` com `is_active(&self, now)->bool`; `Badge::student_valid_until(expected_graduation_year:i32)->OffsetDateTime` (31/12 do ano seguinte, UTC).
  - `DisplayMode::{Publico,Oculto}` (padrão `Oculto`); `AuthorDisplay::compose(input:AuthorDisplayInput)->AuthorDisplay` onde `AuthorDisplayInput { mode, full_name:Option<String>, situation:Option<Situation>, university:Option<String>, badges:Vec<Badge>, stored_badge:Option<BadgeType>, account:AuthorAccountState::{Active,Inactive,Deleted}, now }`; resultado `AuthorDisplay { label:String, badge:Option<BadgeType>, badge_note:Option<&'static str>, public:Option<PublicAuthor> }`; nunca expõe CRM; oculto: `"Autor verificado"` com selo ou `"Autor da comunidade"` sem selo; excluída: `"Autor da comunidade"` com o selo guardado e nota `"na data da publicação"`; inativa: como oculto.
  - `NotificationKind` com `channels()->&[Channel::{Email,Site}]` e `account_related()->bool` (a conta desativada só recebe os ligados à conta).
- [x] Testes: `ac_39_br_08_no_approved_item_means_no_badge`, `ac_40_br_10_primary_badge_follows_order`, `ac_40_br_09_badges_accumulate`, `ac_41_br_13_student_badge_expires_after_graduation_year_plus_one`, `ac_45_br_29_default_display_mode_is_hidden`, `ac_47_br_30_br_31_public_display_never_has_crm`, `ac_48_br_30_hidden_without_badge_is_community_author`, `ac_49_br_32_hidden_with_badge_is_verified_author`, `ac_52_br_34_deleted_author_uses_stored_badge_with_note`, `ac_51_br_31_public_author_has_no_crm_field`, `ac_67_br_42_decision_notifies_email_and_site`, `ac_68_br_42_receipt_notifies_site_only`, `ac_69_br_42_display_mode_changed_notifies_site_only`, `ac_42_br_13_expiring_badge_notifies_email_and_site`.
- [x] Ver falhar, implementar, ver passar, commitar.

## Phase B - Application
- commit: `2fa67b6`

### Task 5: Application auth (estado da conta e equipe)
- layer: application
- repo: medsafari
- depends_on: [1]
- covers: AC-55, AC-58, BR-35, BR-36, BR-37
- test_scope: unit
- files: modificar `crates/application/src/modules/auth/repositories/{user,session}.repository.rs`, `usecases/{session_service,verify_access}.usecase.rs`, `settings.rs` e seus testes existentes; criar `crates/application/src/modules/auth/usecases/principal.usecase.rs` movendo `Principal` com `require_active()` e `require_staff()` e `__tests__/principal.usecase.test.rs`
- verify: `U`
- commit: `feat(application): carry account status and staff flag in the session`
- Interfaces produces: `User` e `SessionRecord` ganham `status: AccountStatus` e `is_staff: bool`; `Principal { user_id, session_id, terms_pending, account_status: AccountStatus, is_staff: bool }` com `require_active(&self)->Result<(),AccessError>` e `require_staff(&self)->Result<(),AccessError>`, `AccessError::{AccountNotActive, NotStaff}`; `UserRepository::reactivate_scheduled_deletion(id: UserId)->Result<(),PortError>`; `VerifyError::AccountSuspended`; `AuthSettings` ganha `institutional_code_valid_minutes: u32 = 15`, `institutional_max_attempts: u8 = 5`, `queue_sla_business_days: u32 = 7`, `deletion_grace_days: i64 = 30`, `export_link_days: i64 = 7`, `export_interval_hours: i64 = 24`, `evidence_retention_days: i64 = 90`, `badge_warning_days: i64 = 30`.
- [x] Testes novos: `ac_58_br_37_verify_cancels_scheduled_deletion`, `br_35_verify_refuses_suspended_account`, `ac_55_br_36_verify_keeps_deactivated_account_and_issues_session`, `ac_35_br_24_require_staff_rejects_regular_principal`, `br_35_require_active_rejects_deactivated`. Atualizar os testes existentes do módulo 01 para os novos campos.
- [x] Ver falhar, implementar, rodar `U` inteiro, commitar.
- commit: `52d1af4`

### Task 6: Application profile
- layer: application
- repo: medsafari
- depends_on: [2, 5]
- covers: AC-01, AC-02, AC-03, AC-04, AC-06, AC-07, AC-08, AC-09, AC-22, BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-17
- test_scope: unit
- files: `crates/application/src/modules/profile/{mod.rs,repositories/{profile,crm_registration,residency,postgraduate,university,specialty}.repository.rs,usecases/{get_profile,update_profile,add_crm_registration,remove_crm_registration,add_residency,remove_residency,add_postgraduate,remove_postgraduate,list_universities,list_specialties}.usecase.rs}` + testes; registrar em `modules/mod.rs` e `lib.rs` conforme o padrão de `auth`
- verify: `U`
- commit: `feat(application): add profile use cases and ports`
- Interfaces produces: portas com `mockall::automock` e `async_trait`; `ProfileRepository::{find(user_id)->Option<StoredProfile>, save(user_id, &Profile)->(), is_name_locked(user_id)->bool}` onde `StoredProfile { profile: Profile, public_id: Uuid, display_mode: DisplayMode, full_name_locked: bool }`; um repositório por tipo de entrada com `list/insert/delete`; `UniversityRepository::{search(q:Option<&str>, limit:u32), exists(id)}`; `SpecialtyRepository::list()`; casos de uso com `execute(&Principal, input)` que chamam `principal.require_active()`; `UpdateProfile` devolve `ProfileUpdateError::NameLocked` quando o nome muda com `full_name_locked`; `GetProfile` devolve o perfil com `complete: bool`.
- [x] Testes: `ac_01_br_01_profile_is_optional_for_empty_profile`, `ac_02_br_02_get_profile_reports_complete`, `ac_22_br_17_locked_name_cannot_change`, `ac_08_br_05_foreign_university_saves_free_text`, `ac_09_br_06_adds_second_crm_in_other_uf`, `ac_06_br_04_update_rejects_oversized_fields`, `br_35_profile_use_cases_reject_deactivated_account`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `aa9e83b`

### Task 7: Application notifications
- layer: application
- repo: medsafari
- depends_on: [4, 5]
- covers: AC-42, AC-54, AC-67, AC-68, AC-69, BR-35, BR-42
- test_scope: unit
- files: `crates/application/src/modules/notifications/{mod.rs,ports/account_mailer.port.rs,repositories/notification.repository.rs,usecases/{dispatch_notification,list_notifications,mark_notification_read}.usecase.rs}` + testes
- verify: `U`
- commit: `feat(application): add notification dispatch`
- Interfaces produces: `AccountMailer::send(to:&Email, kind:&NotificationKind, payload:&NotificationPayload)->Result<(),PortError>`; `NotificationRepository::{insert(NewNotification), list(user_id, limit), mark_read(user_id, id, at)}`; `DispatchNotification::execute(user_id:UserId, to:&Email, account:AccountStatus, kind:NotificationKind, payload)` grava aviso no site quando o canal inclui `Site`, envia e-mail quando inclui `Email` e a conta não é desativada/agendada, ou o tipo é ligado à conta.
- [x] Testes: `ac_67_br_42_dispatches_email_and_site`, `ac_68_br_42_site_only_sends_no_email`, `ac_54_br_35_deactivated_account_gets_only_account_related_email`, `ac_69_br_42_list_returns_own_notifications_only`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `e2840b4`

### Task 8: Application badges
- layer: application
- repo: medsafari
- depends_on: [4, 7]
- covers: AC-15, AC-16, AC-17, AC-18, AC-39, AC-40, AC-41, AC-42, BR-08, BR-09, BR-10, BR-13, BR-19
- test_scope: unit
- files: `crates/application/src/modules/badges/{mod.rs,repositories/badge.repository.rs,usecases/{list_badges,grant_badges_for_verification,expire_student_badges,warn_expiring_student_badges}.usecase.rs}` + testes
- verify: `U`
- commit: `feat(application): add badge granting and expiration`
- Interfaces produces: `BadgeRepository::{insert(NewBadge), list_active(user_id, now), revoke_for_verification(verification_id, at), revoke_all(user_id, at), expiring_students(from, to)->Vec<ExpiringBadge>, mark_warned(badge_id)}`; `GrantBadgesForVerification::execute(&BadgeGrant)` onde `BadgeGrant { user_id, verification_id, badges: Vec<BadgeSpec { kind: BadgeType, detail: Option<String>, valid_until: Option<OffsetDateTime> }> }` apenas grava os selos pedidos (o módulo `badges` não conhece `verification`, regra do teste de arquitetura; quem decide quais selos nascem de cada verificação é `decide_verification`, Task 10); `ListBadges::execute(&Principal)->BadgesView { active: Vec<Badge>, primary: Option<BadgeType> }`; `ExpireStudentBadges::execute()->u64` e `WarnExpiringStudentBadges::execute()->u64` (idempotente por selo).
- [x] Testes: `ac_17_br_19_grant_stores_every_requested_badge_with_detail`, `ac_41_br_13_grant_keeps_valid_until`, `ac_39_br_08_list_without_verified_items_is_empty`, `ac_40_br_10_list_reports_primary_badge`, `ac_41_br_13_expire_revokes_past_valid_until`, `ac_42_br_13_warn_runs_once_per_badge`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `90e09b5`

### Task 9: Application verification (usuário)
- layer: application
- repo: medsafari
- depends_on: [3, 6, 7, 8]
- covers: AC-10, AC-11, AC-12, AC-13, AC-14, AC-19, AC-24, AC-26, AC-28, AC-29, AC-30, AC-31, AC-32, BR-07, BR-11, BR-12, BR-15, BR-20, BR-21, BR-22, BR-23, BR-43
- test_scope: unit
- files: `crates/application/src/modules/verification/{mod.rs,ports/file_storage.port.rs,repositories/{verification,institutional_email_challenge,email_domain}.repository.rs,usecases/{submit_verification,list_my_verifications,request_institutional_code,confirm_institutional_code,purge_expired_evidence}.usecase.rs}` + testes
- verify: `U`
- commit: `feat(application): add user verification use cases`
- Interfaces produces:
  - `FileStorage::{put(key:&str, bytes:Vec<u8>, content_type:&str), get(key:&str)->Option<Vec<u8>>, delete(key:&str)}` (apagar chave inexistente é sucesso).
  - `VerificationRepository::{insert(NewVerification)->VerificationId, find(id), list_for_user(user_id), crm_verified_elsewhere(number, uf, except_user)->bool, update(&Verification), queue(status, limit, offset), expired_evidence(now)->Vec<(Uuid,String)>, clear_file(id)}`; `InstitutionalEmailChallengeRepository::{replace(NewChallenge), find_open(user_id,email), save(&InstitutionalEmailChallenge)}`; `EmailDomainRepository::{university_for_domain(domain)->Option<Uuid>, record_request(user_id, domain, at)}`.
  - `SubmitVerification::execute(&Principal, SubmitInput { item_type, item_id, bytes, content_type })->VerificationId` (valida arquivo, guarda, cria pendente com `crm_conflict` quando o CRM já está verificado em outra conta, notifica "recebido"); `ListMyVerifications` devolve um status por item do perfil, incluindo `NaoEnviado` e motivo da recusa/revogação; `RequestInstitutionalCode::execute(&Principal, email)->Result<(),InstitutionalError>` com `DomainNotListed` (registra pedido de inclusão), `WrongUniversity`; `ConfirmInstitutionalCode::execute(&Principal, email, code)` aprova a matrícula e chama `GrantBadgesForVerification`; `PurgeExpiredEvidence::execute()->u64` apaga arquivo e limpa a chave, mantendo o registro.
- [x] Testes: `ac_28_br_22_submit_rejects_invalid_file`, `ac_14_br_07_submit_creates_pending_and_notifies`, `ac_19_br_15_submit_marks_conflict_when_crm_verified_elsewhere`, `ac_32_br_07_list_reports_not_sent`, `ac_31_br_23_list_shows_rejection_reason_and_allows_resubmission`, `ac_10_br_12_confirm_code_approves_and_grants_student_badge`, `ac_11_br_12_wrong_university_domain_is_rejected`, `ac_13_br_43_unlisted_domain_records_request_and_offers_proof`, `ac_12_br_12_institutional_email_is_not_used_as_login_or_mailing`, `ac_29_br_22_purge_deletes_file_and_keeps_record`, `ac_30_br_22_file_storage_is_only_read_by_staff_use_case`, `ac_24_br_20_residency_submission_is_pending`, `ac_26_br_21_postgraduate_submission_is_pending`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `db591f4`

### Task 10: Application verification (equipe)
- layer: application
- repo: medsafari
- depends_on: [9]
- covers: AC-15, AC-16, AC-17, AC-18, AC-19, AC-20, AC-21, AC-22, AC-23, AC-24, AC-25, AC-26, AC-27, AC-33, AC-34, AC-35, AC-36, AC-37, AC-38, AC-43, AC-44, BR-14, BR-15, BR-16, BR-17, BR-18, BR-19, BR-20, BR-21, BR-23, BR-24, BR-25, BR-26, BR-27, BR-28
- test_scope: unit
- files: `crates/application/src/modules/verification/usecases/{list_verification_queue,get_verification_for_review,decide_verification,revoke_verification,confirm_fraud}.usecase.rs` + testes; `ProfileRepository` ganha `lock_full_name(user_id)` (e mock) e `AccountRepository` é consumido na Task 13 (aqui `confirm_fraud` usa a porta `SuspensionPort` definida em `crates/application/src/modules/verification/repositories/suspension.repository.rs`: `suspend_and_revoke_sessions(user_id, at)`)
- verify: `U`
- commit: `feat(application): add staff verification review use cases`
- Interfaces produces: todos exigem `principal.require_staff()`; `ListVerificationQueue::execute(&Principal)->Vec<QueueItem { id, item_type, submitted_at, overdue:bool, crm_conflict:bool }>` por ordem de chegada; `GetVerificationForReview::execute(&Principal, id)->ReviewView { profile, verification, file_key }` e leitura do arquivo via `FileStorage`; `DecideVerification::{approve(&Principal,id,ApproveInput{observed_status:Option<ObservedCrmStatus>, rqe_specialties:Vec<String>}), reject(&Principal,id,reason:RejectionReason,note:Option<String>)}` — aprovação de CRM exige nome igual (`PersonNameMatch`), situação ativa e ausência de conflito, trava o nome e concede selos; erro `DecisionError::{NameMismatch, NotActive, Conflict, AlreadyDecided, SourceUnavailable}`; indisponibilidade do CFM é informada pela equipe como `SourceUnavailable` e mantém o pedido pendente; `RevokeVerification::execute(&Principal,id,reason:String,observed:Option<ObservedCrmStatus>)` revoga verificação e selos e notifica; `ConfirmFraud::execute(&Principal,user_id,note)` revoga todos os selos, suspende a conta, encerra as sessões e notifica.
- [x] Testes: `ac_33_br_24_queue_is_ordered_by_arrival`, `ac_35_br_24_queue_rejects_non_staff`, `ac_38_br_26_queue_flags_overdue`, `ac_34_br_24_approval_records_decider`, `ac_15_br_17_crm_approval_locks_name`, `ac_16_br_14_non_active_crm_is_refused`, `ac_19_br_15_conflict_blocks_approval`, `ac_20_br_16_name_mismatch_blocks_approval`, `ac_21_br_16_accent_insensitive_name_is_accepted`, `ac_36_br_23_reject_without_reason_is_refused`, `ac_37_br_25_cfm_unavailable_keeps_pending`, `ac_25_br_20_old_residency_declaration_is_refused_as_expired`, `ac_27_br_21_postgraduate_outside_health_is_refused`, `ac_43_br_27_revoke_notifies_with_reason`, `ac_44_br_28_fraud_revokes_everything_and_suspends`, `ac_23_br_18_decision_stores_only_observed_status_and_specialties`, `ac_17_br_19_approval_with_rqe_grants_specialist`, `ac_18_br_19_title_approval_grants_specialist`, `ac_22_br_17_name_change_after_lock_is_blocked`, `ac_24_br_20_residency_approval_grants_resident`, `ac_26_br_21_master_approval_grants_master`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `28810db`

### Task 11: Application privacy
- layer: application
- repo: medsafari
- depends_on: [4, 6, 7, 8]
- covers: AC-45, AC-46, AC-47, AC-48, AC-49, AC-50, AC-51, AC-52, BR-29, BR-30, BR-31, BR-32, BR-33, BR-34
- test_scope: unit
- files: `crates/application/src/modules/privacy/{mod.rs,ports/{public_display_terms_policy,published_questions_counter}.port.rs,repositories/{display_consent,public_author}.repository.rs,usecases/{preview_display,set_display_mode,get_public_author,resolve_author_display}.usecase.rs}` + testes
- verify: `U`
- commit: `feat(application): add display mode and author display`
- Interfaces produces: `PublicDisplayTermsPolicy::current()->DocumentVersion`; `PublishedQuestionsCounter::count(user_id)->Result<u64,PortError>`; `DisplayConsentRepository::{record(user_id, version, ip, at), latest(user_id)->Option<DocumentVersion>}`; `PublicAuthorRepository::{find_by_public_id(Uuid)->Option<AuthorRecord>, find_by_user(UserId)->Option<AuthorRecord>, set_display_mode(user_id, DisplayMode)}`; `PreviewDisplay::execute(&Principal)->{public: AuthorDisplay, hidden: AuthorDisplay}`; `SetDisplayMode::execute(&Principal, mode, accepted: Option<DocumentVersion>, ip)` recusa `Publico` sem aceite igual à versão vigente (`DisplayModeError::ConsentRequired`), grava o aceite, troca o modo e notifica; `ResolveAuthorDisplay::execute(author: UserId, stored_badge: Option<BadgeType>)->AuthorDisplay` (usado pelo módulo 03); `GetPublicAuthor::execute(public_id)->Result<PublicAuthorPage,PublicAuthorError::NotFound>` com `published_questions` do contador.
- [x] Testes: `ac_46_br_29_public_mode_requires_current_terms_acceptance`, `ac_46_br_29_public_mode_with_current_acceptance_is_saved_and_notified`, `ac_45_br_29_new_profile_is_hidden`, `ac_49_br_32_mode_change_applies_to_author_display_immediately`, `ac_50_br_33_preview_shows_both_modes`, `ac_47_br_30_public_page_has_profile_data_and_question_count`, `ac_51_br_31_public_page_never_has_crm`, `ac_48_br_30_resolve_hidden_without_badge`, `ac_52_br_34_resolve_deleted_author_with_stored_badge`, `ac_49_br_30_public_page_is_not_found_when_hidden_or_deactivated`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `4015303`

### Task 12: Application account
- layer: application
- repo: medsafari
- depends_on: [5, 7, 9]
- covers: AC-53, AC-54, AC-55, AC-56, AC-57, AC-58, AC-59, AC-60, AC-61, AC-62, AC-63, AC-64, AC-65, AC-66, BR-35, BR-36, BR-37, BR-38, BR-39, BR-40, BR-41
- test_scope: unit
- files: `crates/application/src/modules/account/{mod.rs,repositories/{account,data_export}.repository.rs,usecases/{deactivate_account,reactivate_account,schedule_account_deletion,execute_due_deletions,request_data_export,download_data_export,purge_expired_exports}.usecase.rs}` + testes
- verify: `U`
- commit: `feat(application): add account lifecycle and data export`
- Interfaces produces: `AccountRepository::{set_status(user_id, AccountStatus, due:Option<OffsetDateTime>)->(), revoke_sessions(user_id, at), due_for_deletion(now, limit)->Vec<DueAccount{user_id,email}>, evidence_keys(user_id)->Vec<String>, erase(user_id)->()}` (`erase` é uma transação: aceites ficam sem `user_id` e sem IP, remove pedidos de acesso do e-mail e o usuário); `DataExportRepository::{last_requested_at(user_id)->Option<OffsetDateTime>, insert(NewExport), find(id), expired(now), delete(id), collect(user_id)->ExportData}`; `DeactivateAccount::execute(&Principal)` (status, sessões revogadas, notificação por e-mail); `ReactivateAccount::execute(&Principal)` aceita conta desativada; `ScheduleAccountDeletion::execute(&Principal, email_confirmation)->OffsetDateTime` recusa e-mail diferente (`DeletionError::EmailMismatch`), usa `deletion_grace_days`; `ExecuteDueDeletions::execute()->u64` apaga arquivos e depois chama `erase`, tolera arquivo já removido e envia o e-mail final; `RequestDataExport::execute(&Principal)->ExportId` recusa com `ExportError::TooSoon` dentro de 24 h, grava o JSON pela `FileStorage` e notifica; `DownloadDataExport::execute(&Principal, id)->Vec<u8>` recusa outra conta ou link expirado com `ExportError::NotFound`; `PurgeExpiredExports::execute()->u64`.
- [x] Testes: `ac_53_br_35_deactivate_sets_status_and_revokes_sessions`, `ac_55_br_36_reactivate_restores_active`, `ac_56_br_37_wrong_confirmation_email_does_not_schedule`, `ac_57_br_37_schedule_sets_due_date_and_notifies`, `ac_59_br_38_execute_deletes_files_then_erases_and_sends_final_email`, `ac_59_br_38_execute_is_idempotent_when_file_is_gone`, `ac_60_br_38_erase_keeps_acceptances_without_identity` (afirmado como chamada da porta com os parâmetros certos), `ac_61_br_39_deletion_is_not_blocked_by_open_disputes`, `ac_62_br_40_deletion_options_include_export_and_deactivate` (consulta `DeletionOptions` com os três destinos), `ac_63_br_41_export_stores_json_and_notifies`, `ac_65_br_41_second_export_within_24h_is_refused`, `ac_64_br_41_download_refuses_other_account`, `ac_66_br_41_download_refuses_expired_link`.
- [x] Ver falhar, implementar, ver passar, commitar.

## Phase C - Migrations e adaptadores Postgres
- commit: `be9c8d7`
- commit (retry do VERIFY, AC-61 e BR-39): `a78da72`

### Task 13: Migrações 0003 e 0004
- layer: adapters-postgres
- repo: medsafari
- depends_on: [1, 2]
- covers: AC-01, AC-09, AC-46, AC-53, AC-59, AC-60, BR-01, BR-06, BR-17, BR-29, BR-35, BR-37, BR-38
- test_scope: unit+integration
- files: `crates/adapters-postgres/migrations/{0003_account_status.sql,0004_profiles_and_reference.sql}`; teste `crates/adapters-postgres/tests/schema.rs` (acrescentar)
- verify: `I`
- commit: `feat(db): add account status, profiles and reference tables`
- Interfaces produces: `users.status text NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa','desativada','exclusao_agendada','suspensa'))`, `users.deletion_due_at timestamptz`, `users.is_staff boolean NOT NULL DEFAULT false`; `terms_acceptances` aceita `'exibicao_publica'`, `user_id` anulável com FK `ON DELETE SET NULL`; tabelas `universities(id uuid pk, name, uf, emec_code)`, `university_email_domains(university_id, domain unique)`, `medical_specialties(id uuid pk, name unique)`, `profiles(user_id pk fk cascade, public_id uuid unique default gen_random_uuid(), full_name, full_name_locked bool, bio, lattes_url, situation, preparing_residency bool, university_id fk null, foreign_university text, admission_year int, graduation_year int, display_mode text default 'oculto' check, updated_at)`, `crm_registrations(id, user_id fk cascade, number, uf, unique(user_id,number,uf))`, `residencies`, `postgraduates` (campos das seções 4.5 e 4.6).
- [x] Testes de integração: `schema_accepts_public_display_document`, `schema_keeps_acceptance_when_user_is_deleted` (user_id vira nulo), `schema_rejects_unknown_account_status`, `schema_profile_defaults_to_hidden_mode`, `schema_applies_all_migrations_from_scratch`.
- [x] Ver falhar (migração inexistente), escrever as migrações, ver passar, commitar.
- commit: `7b61f8a`

### Task 14: Migrações 0005, 0006 e 0007
- layer: adapters-postgres
- repo: medsafari
- depends_on: [13]
- covers: AC-10, AC-19, AC-39, AC-63, AC-67, BR-05, BR-07, BR-12, BR-15, BR-19, BR-41, BR-42, BR-43
- test_scope: unit+integration
- files: `crates/adapters-postgres/migrations/{0005_reference_seed.sql,0006_verifications_and_badges.sql,0007_notifications_and_exports.sql}`; `crates/adapters-postgres/tests/schema.rs` (acrescentar)
- verify: `I`
- commit: `feat(db): add verifications, badges, notifications and exports`
- Interfaces produces: carga de exemplo (3 universidades com domínios, 5 especialidades); `verifications(id, user_id fk cascade, item_type, item_id uuid, method, status, reason, note, file_key, file_delete_at, crm_conflict bool, observed_status, observed_specialties text[], submitted_at, decided_by fk users null, decided_at, issued_at)`; índice único parcial de CRM verificado em `crm_verified(number, uf) WHERE status='aprovado' AND item_type='crm'` (guardar `crm_number`/`crm_uf` na verificação); `institutional_email_challenges`, `email_domain_requests`, `badges(id, user_id fk cascade, type, detail, verification_id fk, valid_until, revoked_at, warned_at)`, `notifications(id, user_id fk cascade, kind, payload jsonb, created_at, read_at)`, `data_exports(id, user_id fk cascade, file_key, requested_at, expires_at)`.
- [x] Testes de integração: `schema_rejects_second_verified_crm_for_same_number_and_uf`, `schema_allows_second_pending_crm_for_same_number_and_uf`, `schema_cascades_verifications_and_badges_on_user_delete`, `schema_seed_has_universities_with_domains`.
- [x] Ver falhar, escrever, ver passar, commitar.
- commit: `7267723`

### Task 15: Postgres auth (status e equipe)
- layer: adapters-postgres
- repo: medsafari
- depends_on: [5, 13]
- covers: AC-55, AC-58, BR-35, BR-36, BR-37
- test_scope: unit+integration
- files: modificar `crates/adapters-postgres/src/modules/auth/repositories/{user,session}.repository.rs`; testes em `crates/adapters-postgres/tests/accounts.rs`
- verify: `I`
- commit: `feat(adapters-postgres): read account status and staff flag with sessions`
- Interfaces produces: consultas de usuário e de sessão trazem `status` e `is_staff` (sessão por junção com `users`); `reactivate_scheduled_deletion` zera `deletion_due_at` e volta o status para `ativa`.
- [x] Testes: `ac_58_br_37_scheduled_deletion_is_cleared`, `ac_55_br_36_session_record_carries_deactivated_status`, `br_35_session_record_carries_staff_flag`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `52d1af4 (junto com a Task 5)`

### Task 16: Postgres profile
- layer: adapters-postgres
- repo: medsafari
- depends_on: [6, 13]
- covers: AC-01, AC-02, AC-08, AC-09, AC-22, BR-01, BR-02, BR-05, BR-06, BR-17
- test_scope: unit+integration
- files: `crates/adapters-postgres/src/modules/profile/{mod.rs,repositories/{profile,crm_registration,residency,postgraduate,university,specialty}.repository.rs}`; `crates/adapters-postgres/tests/profiles.rs`
- verify: `I`
- commit: `feat(adapters-postgres): add profile repositories`
- Interfaces produces: implementações das portas da Task 6 sobre `PgStore`; mapeiam linhas para tipos de domínio sem expor structs de linha; violação de unicidade de CRM vira o erro de adaptador correspondente.
- [x] Testes: `ac_01_br_01_find_without_profile_returns_none`, `ac_02_br_02_save_and_find_roundtrip`, `ac_22_br_17_name_lock_flag_is_returned`, `ac_08_br_05_foreign_university_roundtrip`, `ac_09_br_06_two_crm_registrations_for_one_user`, `br_05_university_search_filters_by_name`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `a09a91c`

### Task 17: Postgres verification e badges
- layer: adapters-postgres
- repo: medsafari
- depends_on: [8, 9, 10, 14]
- covers: AC-10, AC-11, AC-13, AC-14, AC-15, AC-19, AC-29, AC-33, AC-38, AC-39, AC-41, AC-42, AC-43, AC-44, BR-07, BR-12, BR-13, BR-15, BR-22, BR-24, BR-26, BR-27, BR-28, BR-43
- test_scope: unit+integration
- files: `crates/adapters-postgres/src/modules/verification/{mod.rs,repositories/{verification,institutional_email_challenge,email_domain,suspension}.repository.rs}`, `modules/badges/{mod.rs,repositories/badge.repository.rs}`; `crates/adapters-postgres/tests/{verifications,badges}.rs`
- verify: `I`
- commit: `feat(adapters-postgres): add verification and badge repositories`
- Interfaces produces: fila `ORDER BY submitted_at ASC`; `crm_verified_elsewhere` conta CRM aprovado em outra conta; aprovação de CRM trata a violação do índice único como conflito; `SuspensionRepository::suspend_and_revoke_sessions` numa transação; `expired_evidence` retorna chaves com `file_delete_at <= now`.
- [x] Testes: `ac_33_br_24_queue_is_oldest_first`, `ac_19_br_15_concurrent_crm_approval_leaves_one_verified`, `ac_29_br_22_expired_evidence_lists_only_old_decided_files`, `ac_11_br_12_challenge_attempts_are_consumed_atomically`, `ac_13_br_43_domain_request_is_recorded`, `ac_41_br_13_expiring_badges_query_respects_window`, `ac_44_br_28_suspend_revokes_sessions_and_sets_status`, `ac_43_br_27_revoke_for_verification_revokes_derived_badges`, `ac_10_br_12_university_for_domain_lookup`, `ac_14_br_07_insert_and_list_for_user`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `0f7cc0f`

### Task 18: Postgres account, privacy e notifications
- layer: adapters-postgres
- repo: medsafari
- depends_on: [11, 12, 7, 14]
- covers: AC-45, AC-46, AC-49, AC-53, AC-57, AC-59, AC-60, AC-63, AC-65, AC-66, AC-67, AC-69, BR-29, BR-32, BR-35, BR-37, BR-38, BR-41, BR-42
- test_scope: unit+integration
- files: `crates/adapters-postgres/src/modules/account/{mod.rs,repositories/{account,data_export}.repository.rs}`, `modules/privacy/{mod.rs,repositories/{display_consent,public_author}.repository.rs}`, `modules/notifications/{mod.rs,repositories/notification.repository.rs}`; `crates/adapters-postgres/tests/{account,notifications}.rs`
- verify: `I`
- commit: `feat(adapters-postgres): add account, privacy and notification repositories`
- Interfaces produces: `erase` em transação: anula `user_id` e IP em `terms_acceptances`, apaga `login_requests` do e-mail e o usuário (cascata); `due_for_deletion` com `FOR UPDATE SKIP LOCKED`; `collect` monta `ExportData` com conta, perfil, selos, verificações sem arquivos, aceites e tentativas.
- [x] Testes: `ac_59_br_38_erase_removes_user_profile_and_progress`, `ac_60_br_38_erase_keeps_acceptances_without_user_or_ip`, `ac_59_br_38_erase_twice_is_idempotent`, `ac_57_br_37_due_for_deletion_returns_only_overdue_accounts`, `ac_53_br_35_revoke_sessions_revokes_all`, `ac_65_br_41_last_requested_at_is_returned`, `ac_63_br_41_collect_excludes_evidence_files`, `ac_46_br_29_consent_records_and_returns_latest`, `ac_49_br_32_set_display_mode_persists`, `ac_67_br_42_notifications_list_newest_first_and_mark_read`.
- [x] Ver falhar, implementar, ver passar, commitar.

## Phase D - HTTP
- commit: `b3e9d6d`

### Task 19: HTTP base
- layer: adapters-http
- repo: medsafari
- depends_on: [5]
- covers: AC-35, BR-24, BR-35
- test_scope: unit
- files: modificar `crates/adapters-http/src/{error,state,router,openapi,lib}.rs`, `modules/auth/middlewares/require_session.middleware.rs` e os testes existentes; `Cargo.toml` do workspace (`axum` com `multipart`) e do crate
- verify: `U`
- commit: `feat(adapters-http): add shared state, error mappings and session layer for new modules`
- Interfaces produces: `ApiError::{Forbidden, NotFound, Conflict(String), PayloadTooLarge, UnsupportedMediaType, TooManyRequests}` em problem+json; `require_session` passa a usar `State<Arc<SessionService>>`; `AccountApi` e `StaffApi` (structs com `Arc` dos casos de uso, preenchidas nas tarefas seguintes); `account_router(Arc<AccountApi>, Arc<SessionService>)`, `staff_router(Arc<StaffApi>, Arc<SessionService>)`, `public_router(Arc<AccountApi>)` para `GET /api/authors/{public_id}`; `DefaultBodyLimit` de 5 MB + margem nas rotas de upload.
- [x] Testes: `ac_35_br_24_forbidden_maps_to_403_problem_json`, `br_35_not_found_and_conflict_map_to_problem_json`, `br_35_payload_too_large_maps_to_413`, atualizar `require_session` e `router` tests para o novo estado.
- [x] Ver falhar, implementar, rodar `U` inteiro, commitar.
- commit: `c215b04`

### Task 20: HTTP profile e badges
- layer: adapters-http
- repo: medsafari
- depends_on: [6, 8, 19]
- covers: AC-01, AC-02, AC-03, AC-04, AC-06, AC-07, AC-08, AC-09, AC-22, AC-39, AC-40, BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-08, BR-09, BR-10, BR-17
- test_scope: unit
- files: `crates/adapters-http/src/modules/profile/{mod.rs,controllers/{profile,crm_registration,residency,postgraduate,reference}.controller.rs,dtos/{profile,crm_registration,residency,postgraduate,reference}.dto.rs}`, `modules/badges/{mod.rs,controllers/badge.controller.rs,dtos/badge.dto.rs}` + testes (`tower::ServiceExt::oneshot` com caso de uso falso)
- verify: `U`
- commit: `feat(adapters-http): add profile and badge routes`
- Interfaces produces: `GET/PUT /api/profile`, `POST /api/profile/crm-registrations`, `DELETE /api/profile/crm-registrations/{id}`, rotas análogas para `residencies` e `postgraduates`, `GET /api/reference/universities`, `GET /api/reference/specialties`, `GET /api/badges`; DTOs `ToSchema`; `409` para nome travado; `422` para validação; anotações `utoipa::path`.
- [x] Testes: `ac_01_br_01_get_profile_returns_incomplete_flag`, `ac_06_br_04_put_profile_oversized_is_422`, `ac_22_br_17_put_profile_locked_name_is_409`, `ac_09_br_06_post_crm_returns_201`, `ac_39_br_08_get_badges_empty`, `ac_40_br_10_get_badges_includes_primary`, `br_35_deactivated_principal_gets_403_on_profile`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `ea8d2ba`

### Task 21: HTTP verification (usuário)
- layer: adapters-http
- repo: medsafari
- depends_on: [9, 19]
- covers: AC-10, AC-11, AC-13, AC-14, AC-28, AC-31, AC-32, BR-07, BR-12, BR-22, BR-23, BR-43
- test_scope: unit
- files: `crates/adapters-http/src/modules/verification/{mod.rs,controllers/{verification,institutional_email}.controller.rs,dtos/{verification,institutional_email}.dto.rs}` + testes
- verify: `U`
- commit: `feat(adapters-http): add user verification routes`
- Interfaces produces: `GET /api/verifications`, `POST /api/verifications` (multipart: `item_type`, `item_id`, `file`), `POST /api/verifications/institutional-email`, `POST /api/verifications/institutional-email/confirm`; `413` acima do limite, `415` para tipo recusado, `409` com `offer_proof: true` para domínio fora da lista, `422` para domínio de outra universidade.
- [x] Testes: `ac_28_br_22_upload_over_limit_is_413`, `ac_28_br_22_upload_with_wrong_content_is_415`, `ac_14_br_07_upload_returns_201_pending`, `ac_13_br_43_unlisted_domain_is_409_offering_proof`, `ac_11_br_12_wrong_university_is_422`, `ac_10_br_12_confirm_returns_200`, `ac_32_br_07_list_reports_not_sent`, `ac_31_br_23_list_includes_reason`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `8ca2a1c`

### Task 22: HTTP staff
- layer: adapters-http
- repo: medsafari
- depends_on: [10, 19]
- covers: AC-15, AC-16, AC-19, AC-20, AC-33, AC-34, AC-35, AC-36, AC-37, AC-38, AC-43, AC-44, BR-14, BR-15, BR-16, BR-23, BR-24, BR-25, BR-26, BR-27, BR-28
- test_scope: unit
- files: `crates/adapters-http/src/modules/staff/{mod.rs,controllers/{verification_queue,verification_review,verification_decision,fraud,domain_request}.controller.rs,dtos/{verification_queue,verification_review,decision,fraud,domain_request}.dto.rs}` + testes
- verify: `U`
- commit: `feat(adapters-http): add staff review routes`
- Interfaces produces: `GET /api/staff/verifications`, `GET /api/staff/verifications/{id}`, `GET /api/staff/verifications/{id}/file`, `POST .../approve`, `POST .../reject`, `POST .../revoke`, `POST /api/staff/users/{user_id}/fraud`, `GET /api/staff/domain-requests`; `403` para quem não é equipe; `409` para conflito e decisão repetida; `422` para recusa sem motivo.
- [x] Testes: `ac_35_br_24_queue_is_403_for_regular_user`, `ac_33_br_24_queue_includes_overdue_and_conflict_flags`, `ac_34_br_24_approve_returns_204`, `ac_19_br_15_approve_with_conflict_is_409`, `ac_20_br_16_approve_with_name_mismatch_is_422`, `ac_16_br_14_approve_with_non_active_status_is_422`, `ac_36_br_23_reject_without_reason_is_422`, `ac_37_br_25_source_unavailable_keeps_pending_200`, `ac_43_br_27_revoke_returns_204`, `ac_44_br_28_fraud_returns_204`, `ac_38_br_26_overdue_flag_in_queue_dto`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `4162845`

### Task 23: HTTP privacy, account e notifications
- layer: adapters-http
- repo: medsafari
- depends_on: [11, 12, 7, 19]
- covers: AC-42, AC-45, AC-46, AC-47, AC-48, AC-49, AC-50, AC-51, AC-52, AC-53, AC-55, AC-56, AC-57, AC-62, AC-63, AC-64, AC-65, AC-66, AC-67, AC-68, AC-69, BR-29, BR-30, BR-31, BR-32, BR-33, BR-34, BR-35, BR-36, BR-37, BR-40, BR-41, BR-42
- test_scope: unit
- files: `crates/adapters-http/src/modules/privacy/{mod.rs,controllers/{privacy,public_author}.controller.rs,dtos/{privacy,public_author}.dto.rs}`, `modules/account/{mod.rs,controllers/{account,data_export}.controller.rs,dtos/{account,data_export}.dto.rs}`, `modules/notifications/{mod.rs,controllers/notification.controller.rs,dtos/notification.dto.rs}` + testes; `GET /api/auth/session` passa a devolver `account_status` e `is_staff` (modificar `session.dto.rs` e teste)
- verify: `U`
- commit: `feat(adapters-http): add privacy, account and notification routes`
- Interfaces produces: `GET /api/privacy/preview`, `PUT /api/privacy/display-mode`, `GET /api/authors/{public_id}` (pública), `POST /api/account/{deactivate,reactivate,deletion,exports}`, `GET /api/account/exports/{id}/download`, `GET /api/account/deletion-options` (exportar, desativar, minhas questões), `GET /api/notifications`, `POST /api/notifications/{id}/read`; `422` sem aceite; `429` para exportação repetida; `404` para link expirado ou de outra conta; `401` sem sessão.
- [x] Testes: `ac_46_br_29_public_mode_without_acceptance_is_422`, `ac_50_br_33_preview_returns_both_modes`, `ac_47_br_30_public_page_has_no_crm`, `ac_49_br_30_public_page_hidden_is_404`, `ac_53_br_35_deactivate_returns_204`, `ac_55_br_36_reactivate_allowed_for_deactivated_principal`, `ac_56_br_37_wrong_email_is_422`, `ac_57_br_37_deletion_returns_202_with_due_date`, `ac_62_br_40_deletion_options_lists_three_destinations`, `ac_65_br_41_second_export_is_429`, `ac_64_br_41_download_without_session_is_401`, `ac_66_br_41_expired_download_is_404`, `ac_67_br_42_notifications_list_and_mark_read`, `ac_52_br_34_resolve_author_for_deleted_author_is_community`, `ac_48_br_30_session_returns_account_status`.
- [x] Ver falhar, implementar, ver passar, commitar.

## Phase E - Bootstrap, ferramentas e fluxo completo
- commit: `de3f184`

### Task 24: Bootstrap providers e config
- layer: bootstrap
- repo: medsafari
- depends_on: [9, 11, 7]
- covers: AC-28, AC-29, AC-30, AC-46, AC-67, BR-22, BR-29, BR-30, BR-42
- test_scope: unit
- files: `crates/bootstrap/src/config.rs`; `crates/bootstrap/src/modules/verification/providers/{mod.rs,local_file_storage.provider.rs}`, `modules/notifications/providers/{mod.rs,log_account_mailer.provider.rs}`, `modules/privacy/providers/{mod.rs,env_public_display_terms.provider.rs,zero_published_questions.provider.rs}` + testes
- verify: `U`
- commit: `feat(bootstrap): add storage, mailer and display terms providers`
- Interfaces produces: `Config` ganha `public_display_terms_version: String` (`PUBLIC_DISPLAY_TERMS_VERSION`, obrigatório) e `storage_dir: PathBuf` (`STORAGE_DIR`, padrão `./storage`); `LocalFileStorage::new(root:PathBuf)` implementa `FileStorage` aceitando só chaves `[A-Za-z0-9_-]` (recusa `/`, `..` e vazio), cria o diretório, escreve com permissão `0600`; `LogAccountMailer` registra o evento sem dados pessoais além do tipo; `EnvPublicDisplayTerms`; `ZeroPublishedQuestions`. `dev/init-env.sh` ganha as duas variáveis.
- [x] Testes: `config_requires_public_display_terms_version`, `ac_30_br_22_storage_rejects_path_traversal_keys`, `ac_28_br_22_storage_roundtrip_in_temp_dir`, `ac_29_br_22_storage_delete_missing_key_is_ok`, `ac_67_br_42_log_mailer_does_not_log_email_body`, `ac_46_br_29_env_terms_version_blank_is_rejected`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `f4282bd`

### Task 25: Bootstrap wiring
- layer: bootstrap
- repo: medsafari
- depends_on: [20, 21, 22, 23, 24]
- covers: AC-01, AC-14, AC-33, AC-45, AC-53, AC-63, BR-01, BR-07, BR-24, BR-29, BR-35, BR-41
- test_scope: unit
- files: `crates/bootstrap/src/modules/{profile,verification,badges,privacy,account,notifications}/{mod.rs,<modulo>.module.rs}`, `crates/bootstrap/src/{wiring.rs,lib.rs}` + `__tests__/wiring.test.rs` (acrescentar)
- verify: `U`
- commit: `feat(bootstrap): wire profile, verification, badges, privacy, account and notifications`
- Interfaces produces: cada `<modulo>.module.rs` expõe `build(...)` com os casos de uso; `build_router` junta `health`, `auth_router`, `account_router`, `staff_router` e `public_router`; `build_router_with_email` mantém a assinatura e usa `LogAccountMailer` e `LocalFileStorage` por padrão; `build_router_with_ports` (novo) permite injetar mailer e storage nos testes de fluxo.
- [x] Testes: `wiring_exposes_profile_route`, `wiring_exposes_staff_route_protected`, `wiring_exposes_public_author_route_without_session`.
- [x] Ver falhar, implementar, rodar `U` inteiro, commitar.
- commit: `edc74ce`

### Task 26: Bootstrap jobs
- layer: bootstrap
- repo: medsafari
- depends_on: [25]
- covers: AC-29, AC-41, AC-42, AC-59, AC-66, BR-13, BR-22, BR-37, BR-38, BR-41
- test_scope: unit
- files: `crates/bootstrap/src/bin/jobs.rs`, `crates/bootstrap/src/jobs.rs` + `crates/bootstrap/src/__tests__/jobs.test.rs`; `crates/bootstrap/Cargo.toml` (`[[bin]]`)
- verify: `U`
- commit: `feat(bootstrap): add one-shot jobs binary`
- Interfaces produces: `enum Job { PurgeEvidence, ExecuteDeletions, ExpireBadges, WarnBadges, PurgeExports }` com `Job::parse(&str)` (`purge-evidence`, `execute-deletions`, `expire-badges`, `warn-badges`, `purge-exports`); `run(job: Job, ...)->Result<u64, JobError>` que imprime quantos itens processou; `bin/jobs.rs` só lê config, conecta e chama `run` (mesmo padrão de `bin/migrate.rs`).
- [x] Testes: `job_parse_accepts_all_names`, `job_parse_rejects_unknown_name`, `ac_29_br_22_purge_evidence_job_calls_use_case`.
- [x] Ver falhar, implementar, ver passar, commitar.
- commit: `8ebb7c8`

### Task 27: Ferramentas e documentação
- layer: bootstrap
- repo: medsafari
- depends_on: [25]
- covers: AC-33, AC-34, AC-35, BR-24
- test_scope: unit
- files: `dev/create-staff.sh`, `docs/requests.http`, `docs/subir-e-testar-o-backend.md`
- verify: `bash -n dev/create-staff.sh` e `shellcheck dev/create-staff.sh` quando disponível
- commit: `chore(dev): add staff account script and docs for the new routes`
- Interfaces produces: `dev/create-staff.sh <email>` cria (ou promove) o usuário com `is_staff = true`, `email_verified_at = now()` e perfil vazio, usando o Postgres de `dev/db.sh` via `podman exec`, e recusa e-mail vazio ou com aspas; `docs/subir-e-testar-o-backend.md` explica o agendamento dos cinco subcomandos de `jobs` e as variáveis novas.
- [x] Verificar: rodar o script contra o Postgres de `dev/db.sh up`, conferir `SELECT is_staff FROM users`, rodar duas vezes (idempotente) e commitar.
- commit: `696bdcd`

### Task 28: Fluxo completo e arquitetura
- layer: bootstrap
- repo: medsafari
- depends_on: [25, 26]
- covers: AC-01, AC-10, AC-14, AC-15, AC-17, AC-19, AC-33, AC-34, AC-35, AC-40, AC-46, AC-49, AC-53, AC-55, AC-57, AC-58, AC-59, AC-60, AC-63, AC-64, AC-65, AC-43, AC-44, BR-01, BR-07, BR-14, BR-15, BR-24, BR-28, BR-29, BR-32, BR-35, BR-36, BR-37, BR-38, BR-41
- test_scope: unit+integration
- files: `crates/bootstrap/tests/{account_flow,staff_flow}.rs`; `.config/nextest.toml` (os dois binários entram em `integration` e saem de `unit`); `crates/bootstrap/tests/architecture.rs` (conferir que novos módulos respeitam a regra)
- verify: `U` e `I`
- commit: `test(bootstrap): add account and staff end-to-end flows`
- Interfaces produces: `account_flow` sobe API + Postgres (testcontainers) com mailer e storage de teste e cobre: perfil completo → envio de CRM → aprovação pela conta de equipe → selo Médico → modo público com aceite → página pública sem CRM → desativar → login pede reativação → reativar → agendar exclusão → entrar cancela → agendar de novo, vencer o prazo e executar `ExecuteDueDeletions` → aceites sem identidade, questões não existem; `staff_flow` cobre fila, conflito de CRM entre duas contas, recusa com motivo, revogação e fraude; exportação: pedido, segundo pedido em 24 h recusado, download por outra conta negado.
- [x] Testes: `ac_15_br_14_crm_approved_end_to_end`, `ac_19_br_15_second_account_gets_conflict`, `ac_46_br_29_public_page_requires_consent`, `ac_53_br_35_deactivate_then_reactivate_end_to_end`, `ac_58_br_37_login_cancels_scheduled_deletion`, `ac_59_br_38_deletion_job_erases_personal_data_and_keeps_acceptances`, `ac_65_br_41_export_rate_limit_end_to_end`, `ac_44_br_28_fraud_suspends_account_and_blocks_login`.
- [x] Ver falhar, implementar o que faltar, rodar `U` e `I` inteiros, commitar.
- commit: `0dbf233`

---

## Cobertura e notas de fechamento

- Cada AC (01 a 69) e BR (01 a 43) aparece no `covers` de ao menos uma tarefa; a conferência é feita por script no fim do plano, antes de pedir a aprovação.
- A decisão de comparação de nomes por tabela própria de acentos (e não por `unicode-normalization`) preserva a regra de domínio sem dependência nova; está registrada em Global Constraints.
- Itens fora do escopo, confirmados no refino: telas, tabela `questions`, comentários e contestações, denúncia de histórico e webservice do CFM.
