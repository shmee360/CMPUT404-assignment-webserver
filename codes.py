# Copyright 2021 Warren Stix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

RESP = {
    200: '200 OK\r\nConnection: close\r\n',
    301: '301 Moved Permanently\r\nLocation: %s\r\nConnection: close\r\n',
    302: '302 Found\r\nConnection: close\r\n',
    404: '404 Not Found\r\nConnection: close\r\n',
    405: '405 Method Not Allowed\r\nAllow: GET\r\nConnection: close\r\n',
}
