# Background-completion wake validation

Base: `5bf0d2fb8c728932fdbc6b49a24113aebc2a4ddd`. Implementation: `b6994ac05fcc656c0105b2d94d6acb8518ca098c`.
Final head `9b09a1a9f481616f2c7074bda7c711874038794d` only tightens the shell test to wait for output drainage; both changed parameter cases passed separately.

Local environment: Windows 10, Python 3.13.15. Focused suite: 78 passed. Full Python suite: 3,040 passed, 56 failed, 6 errors, 65 skipped (719.09 seconds).

All 62 failed/error nodes were rerun on a clean checkout of the base using the same interpreter and dependencies. 54 failed and 6 errored there too; the other 2 passed both on the base and on a separate patched rerun. This does not claim that the full suite is green or that parallel execution is equivalent to serial CI.

The first full run stalled in pytest's assertion diff formatter. The completed rerun used `python -m pytest tests -v -n 4 --dist=loadfile --tb=short --assert=plain`. Baseline comparison used the same flags with two workers and only the failed/error node IDs. Plain assertions retain the assertions while disabling pytest's expression rewriting.

GUI typecheck passed. GUI unit suite: 55 files / 541 tests passed. Local GUI E2E: 345 passed / 1 failed (`automation-toast.spec.ts:20`); its 20-repeat check produced 18 passed / 2 failed. GUI files are unchanged from the base.

## Failed/error nodes compared with the clean base

| Node | Patched full run | Clean base rerun |
| --- | --- | --- |
| `tests/test_automation.py::test_compute_next_run_once_local_is_dst_aware` | FAILED | FAILED |
| `tests/test_base_dir.py::test_confined_paths_resolve_under_base_and_outsiders_are_refused` | FAILED | FAILED |
| `tests/test_board_image_lifecycle.py::test_concurrent_identical_uploads_dedupe_without_shared_temp_race` | FAILED | FAILED |
| `tests/test_board_image_lifecycle.py::test_escape_and_symlink_to_ungranted_file_are_denied` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_install_script_downloads_the_program_on_a_mac` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_install_script_is_valid_posix_shell_and_runs_nothing_if_truncated` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_install_script_refuses_an_unsupported_os` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_macos_service_install_refuses_a_twin_on_the_same_state_dir` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_macos_service_install_writes_a_launchd_agent` | FAILED | FAILED |
| `tests/test_cli_surface.py::test_service_needs_a_joined_machine_and_a_supported_platform` | FAILED | FAILED |
| `tests/test_config.py::test_workspace_trust_is_canonical_and_user_owned` | FAILED | FAILED |
| `tests/test_configured_spawn.py::test_swe_lead_is_reachable_on_github_and_slack` | FAILED | FAILED |
| `tests/test_environment.py::test_context_with_git_repo` | FAILED | PASSED; patched isolated rerun also passed |
| `tests/test_gallery_contract.py::test_approval_prompt_data_matches_the_gallery` | ERROR | ERROR |
| `tests/test_gallery_contract.py::test_connector_request_payload_matches_the_gallery` | ERROR | ERROR |
| `tests/test_gallery_contract.py::test_lead_decision_payload_matches_the_gallery` | ERROR | ERROR |
| `tests/test_gallery_contract.py::test_question_fields_match_the_gallery` | ERROR | ERROR |
| `tests/test_gallery_contract.py::test_staffing_card_payload_matches_the_gallery` | ERROR | ERROR |
| `tests/test_gallery_contract.py::test_work_items_payload_matches_the_gallery` | ERROR | ERROR |
| `tests/test_github_installs.py::test_one_hub_fans_out_to_both_adapters` | FAILED | FAILED |
| `tests/test_headless_run.py::test_run_help_and_the_top_level_help_mention_the_command` | FAILED | FAILED |
| `tests/test_headless_run.py::test_the_task_can_be_piped_in_on_standard_input` | FAILED | FAILED |
| `tests/test_mcp.py::test_connect_mcp_failure_includes_stderr_tail` | FAILED | FAILED |
| `tests/test_mcp.py::test_prepare_records_failure_status_and_session_notice` | FAILED | FAILED |
| `tests/test_mcp.py::test_stdio_startup_crash_captures_stderr_tail` | FAILED | FAILED |
| `tests/test_projects.py::TestProjectKey::test_label_home_collapse` | FAILED | FAILED |
| `tests/test_proposal_contract.py::test_domain_examples_are_valid_tool_arguments` | FAILED | FAILED |
| `tests/test_provenance.py::test_device_symlink_is_ignored_but_regular_null_named_script_is_not` | FAILED | FAILED |
| `tests/test_remote_home.py::test_cloud_proxy_union_end_to_end` | FAILED | PASSED; patched isolated rerun also passed |
| `tests/test_remote_home.py::test_identity_created_once_and_private` | FAILED | FAILED |
| `tests/test_remote_home.py::test_sealing_round_trip_and_tamper` | FAILED | FAILED |
| `tests/test_run_cli.py::test_a_command_card_offers_once_this_session_and_no` | FAILED | FAILED |
| `tests/test_run_cli.py::test_a_folder_request_is_asked_and_yes_gives_the_folder` | FAILED | FAILED |
| `tests/test_run_cli.py::test_the_retry_line_says_why_the_model_call_failed` | FAILED | FAILED |
| `tests/test_run_cli.py::test_with_auto_answer_a_folder_request_is_declined_by_rule` | FAILED | FAILED |
| `tests/test_sandbox_settings.py::test_a_missing_base_image_shows_as_needs_download_not_as_ready` | FAILED | FAILED |
| `tests/test_security_bundles.py::test_cloud_posture_drives_trivy_config_not_deprecated_tfsec` | FAILED | FAILED |
| `tests/test_security_bundles.py::test_scanner_skills_offer_a_fallback_instead_of_stopping` | FAILED | FAILED |
| `tests/test_server.py::test_workspace_command_trust_controls_live_engine` | FAILED | FAILED |
| `tests/test_shell_env_isolation.py::test_explicit_env_overrides_still_apply` | FAILED | FAILED |
| `tests/test_shell_env_isolation.py::test_sandbox_runner_still_inherits_its_parent_environment` | FAILED | FAILED |
| `tests/test_shell_env_isolation.py::test_the_users_own_keys_are_still_available` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_carries_the_broker_target_session` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_carries_the_routed_coworker` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_dispatches_team_qualified_event` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_nudge_pulls_history` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_two_workspace_fan_in` | FAILED | FAILED |
| `tests/test_slack_relay.py::test_relay_watchdog_reconnects` | FAILED | FAILED |
| `tests/test_statelock.py::test_lock_is_held_across_processes_and_names_the_holder` | FAILED | FAILED |
| `tests/test_statelock.py::test_second_acquire_in_process_is_refused_with_holder_pid` | FAILED | FAILED |
| `tests/test_team_file_artifacts.py::test_text_pages_pin_version_and_replay` | FAILED | FAILED |
| `tests/test_team_git_handoff.py::test_software_personas_require_verified_owner_handoff[swe-lead]` | FAILED | FAILED |
| `tests/test_team_git_handoff.py::test_software_personas_require_verified_owner_handoff[swe-worker]` | FAILED | FAILED |
| `tests/test_team_git_handoff.py::test_software_personas_require_verified_owner_handoff[test-worker]` | FAILED | FAILED |
| `tests/test_team_rehearsal_fixes.py::test_runtime_facts_do_not_read_configuration_or_follow_workspace_symlinks` | FAILED | FAILED |
| `tests/test_tool_request.py::test_decline_recheck_finds_a_copy_the_user_installed_themselves` | FAILED | FAILED |
| `tests/test_tool_request.py::test_declining_tells_the_agent_to_fall_back_openly` | FAILED | FAILED |
| `tests/test_tool_request.py::test_emits_tool_requested_and_reports_install` | FAILED | FAILED |
| `tests/test_toolchain.py::test_install_writes_a_verified_binary` | FAILED | FAILED |
| `tests/test_toolchain.py::test_missing_reports_only_absent_tools` | FAILED | FAILED |
| `tests/test_toolchain.py::test_resolve_prefers_path` | FAILED | FAILED |
| `tests/test_toolchain.py::test_resolve_returns_absolute_path` | FAILED | FAILED |
