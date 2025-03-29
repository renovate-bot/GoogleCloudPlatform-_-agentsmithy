# Copyright 2025 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Data source to get project numbers
resource "null_resource" "increment_counter" {
  count = var.increment_runs ? 1 : 0

  triggers = {
    any_change = timestamp()
  }

  provisioner "local-exec" {
    command = "curl -X POST \"${var.cloud_function_runs_counter_url}\""
  }
}