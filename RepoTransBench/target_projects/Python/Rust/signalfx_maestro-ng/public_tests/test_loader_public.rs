use std::fs;
use std::io::Write;
use std::env;
use tempfile::tempdir;
use std::collections::HashMap;

// Dummy error type
#[derive(Debug)]
struct DummyMaestroException(String);

fn load_services_from_file(filename: &str) -> Result<HashMap<String, serde_yaml::Value>, DummyMaestroException> {
    if filename.ends_with(".txt") {
        return Err(DummyMaestroException("Unsupported file format".to_string()));
    }
    if !std::path::Path::new(filename).exists() {
        return Err(DummyMaestroException("File not found".to_string()));
    }
    let content = std::fs::read_to_string(filename).map_err(|_| DummyMaestroException("File not found".to_string()))?;
    let mut data: HashMap<String, serde_yaml::Value> = serde_yaml::from_str(&content).map_err(|_| DummyMaestroException("Invalid YAML".to_string()))?;
    for (_service, conf) in data.iter_mut() {
        if let Some(env_list) = conf.get_mut("environment") {
            if let Some(env_vars) = env_list.as_sequence_mut() {
                let mut new_env = vec![];
                for var in env_vars.iter() {
                    if let Some(varstr) = var.as_str() {
                        if let Some(start) = varstr.find("${") {
                            let var_name = &varstr[start + 2..varstr.find("}").unwrap()];
                            let val = env::var(var_name).unwrap_or_else(|_| "".to_string());
                            let prefix = varstr.split('=').next().unwrap();
                            new_env.push(format!("{}={}", prefix, val));
                        } else {
                            new_env.push(varstr.to_string());
                        }
                    }
                }
                let vals: Vec<serde_yaml::Value> = new_env.into_iter().map(serde_yaml::Value::String).collect();
                *env_vars = vals;
            }
        }
    }
    Ok(data)
}

#[test]
fn test_load_invalid_file_extension() {
    let res = load_services_from_file("invalid_format.txt");
    assert!(res.is_err());
}

#[test]
fn test_load_missing_file() {
    let res = load_services_from_file("this_file_does_not_exist_public.yaml");
    assert!(res.is_err());
}

#[test]
fn test_load_env_variable_substitution_public() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("service_env_public.yaml");
    let mut file = fs::File::create(&file_path).unwrap();
    writeln!(
        file,
        "serviceA:\n  image: \"public_image:tag\"\n  environment:\n    - PUBLIC_VAR=${{PUBLIC_VAR_TEST}}"
    )
    .unwrap();
    env::set_var("PUBLIC_VAR_TEST", "public_test_value");
    let config = load_services_from_file(file_path.to_str().unwrap()).unwrap();
    let env_list = config
        .get("serviceA")
        .unwrap()
        .get("environment")
        .unwrap()
        .as_sequence()
        .unwrap();
    assert_eq!(env_list[0], serde_yaml::Value::String("PUBLIC_VAR=public_test_value".to_string()));
}

#[test]
fn test_load_invalid_yaml_syntax() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("broken_config_public.yaml");
    let mut file = fs::File::create(&file_path).unwrap();
    writeln!(
        file,
        "serviceB:\n  image: \"repo/image\n  environment:\n    - INVALID"
    )
    .unwrap();
    let res = load_services_from_file(file_path.to_str().unwrap());
    assert!(res.is_err());
}