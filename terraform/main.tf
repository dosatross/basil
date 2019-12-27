
resource "random_id" "id-suffix" {
  byte_length = 4
}

provider "google" {
  project = "basil-234800"
}

resource "google_sql_database_instance" "basil-postgres" {
  name = "basil-postgres-${random_id.id-suffix.hex}"
  database_version = "POSTGRES_9_6"
  region = "australia-southeast1"

  settings {
    tier = "db-f1-micro"
    disk_type = "PD_HDD"
    disk_size = "10"
    disk_autoresize = true
    availability_type = "ZONAL"
  }
}

resource "google_sql_database" "basil-postgres" {
  name = "basil-postgres"
  instance = "${google_sql_database_instance.basil-postgres.name}"
}

resource "google_sql_user" "user-postgres" {
  name     = "postgres"
  instance = "${google_sql_database_instance.basil-postgres.name}"
  password = "password"
}

