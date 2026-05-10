const fs = require('fs');
const filepath = '/workspace/video-kitchen-2.1/recipes/public/index.html';
let html = fs.readFileSync(filepath, 'utf8');

const newCard = `
                <!-- Opener Preview Card -->
                <div class="card p-6 rounded-lg flex flex-col h-full bg-[#111] border-gray-800">
                    <div class="flex justify-between items-start mb-4">
                        <h2 class="text-xl font-bold text-white">FFWD Opener (WebM)</h2>
                        <span class="bg-blue-900 text-blue-300 px-2 py-1 rounded text-xs uppercase font-bold">Standard CI</span>
                    </div>
                    <p class="text-gray-400 mb-4 text-sm">Transparent animated WebM overlay for the standard FFWD opener sequence.</p>
                    
                    <div class="w-full bg-[#000] border border-gray-700 rounded overflow-hidden relative mb-4 iframe-wrapper" style="aspect-ratio: 16/9;">
                        <iframe src="preview-opener.html" class="absolute top-0 left-0 w-[1920px] h-[1080px] pointer-events-none origin-top-left scaled-iframe"></iframe>
                    </div>
                    
                    <div class="mt-auto flex gap-2">
                        <button class="w-1/2 text-center py-2 bg-gray-800 hover:bg-gray-700 text-white font-semibold rounded transition text-xs">Copy HTML Tag</button>
                        <button class="w-1/2 text-center py-2 bg-gray-800 hover:bg-gray-700 text-white font-semibold rounded transition text-xs">Edit Mapping</button>
                    </div>
                </div>
`;

html = html.replace(/(<div id="tab-design" class="tab-content">[\s\S]*?<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">)/, '$1' + newCard);

html = html.replace("const wrapper = document.getElementById('iframe-wrapper');", "const wrappers = document.querySelectorAll('.iframe-wrapper');");
html = html.replace("const iframe = document.getElementById('scaled-iframe');", "const iframes = document.querySelectorAll('.scaled-iframe');");
html = html.replace(`if(wrapper && iframe) {
                                const scale = wrapper.clientWidth / 1920;
                                iframe.style.transform = \\\`scale(\\\${scale})\\\`;
                            }`, `wrappers.forEach((wrapper, index) => {
                                const scale = wrapper.clientWidth / 1920;
                                if(iframes[index]) iframes[index].style.transform = \`scale(\${scale})\`;
                            });`);

html = html.replace(/id="iframe-wrapper"/g, '');
html = html.replace(/id="scaled-iframe"/g, '');

// Make sure classes are right
html = html.replace('class="w-full bg-[#000] border border-gray-700 rounded overflow-hidden relative mb-4"', 'class="w-full bg-[#000] border border-gray-700 rounded overflow-hidden relative mb-4 iframe-wrapper"');
html = html.replace('class="absolute top-0 left-0 w-[1920px] h-[1080px] pointer-events-none origin-top-left"', 'class="absolute top-0 left-0 w-[1920px] h-[1080px] pointer-events-none origin-top-left scaled-iframe"');

fs.writeFileSync(filepath, html);
