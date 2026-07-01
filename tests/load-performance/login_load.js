import http from 'k6/http';
import { check } from 'k6';

export const options = { vus: 500, duration: '2m' };

export default function () {
  const res = http.post('https://staging.identitysec.internal/api/login', JSON.stringify({ username: 'loadtest', password: 'loadtest' }));
  check(res, { 'status is 200': (r) => r.status === 200 });
}
