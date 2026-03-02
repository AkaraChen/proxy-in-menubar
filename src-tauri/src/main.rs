// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod command;
mod fns;
mod tray;

use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            command::init,
            command::show_menubar_panel
        ])
        .plugin(tauri_nspanel::init())
        .setup(|app| {
            app.set_activation_policy(tauri::ActivationPolicy::Accessory);

            let app_handle = app.app_handle();

            // Resolve paths to Python and server.py
            let python_path = app_handle
                .path()
                .resolve(
                    "resources/python/bin/python3",
                    tauri::path::BaseDirectory::Resource,
                )
                .expect("failed to resolve python path");

            let server_path = app_handle
                .path()
                .resolve("resources/server.py", tauri::path::BaseDirectory::Resource)
                .expect("failed to resolve server path");

            println!("Python path: {:?}", python_path);
            println!("Server path: {:?}", server_path);

            // Spawn Python server
            std::process::Command::new(python_path)
                .arg(server_path)
                .spawn()
                .expect("failed to spawn python server");

            tray::create(app_handle)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
