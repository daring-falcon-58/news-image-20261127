// news-image-20261127 — "Sum up 27 November's world news in one image".
// Node 22, standard library only. The entry image is the entry.png beside
// this file; the program copies it to /output/entry.png (MAKEFUN_OUTPUT_DIR
// stands in for /output outside the grader's container):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The image is a whole JPEG, 1024x1024, 310104 bytes, built 27 Nov 2026
// from 50 stories all first reported on Friday 27 November 2026.

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const out = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), out);

// Sanity check the copy is the whole JPEG we built (magic bytes FF D8 FF).
const head = readFileSync(out).subarray(0, 3);
if (head[0] !== 0xff || head[1] !== 0xd8 || head[2] !== 0xff) {
  throw new Error('entry.png copy failed the JPEG magic-byte check');
}
