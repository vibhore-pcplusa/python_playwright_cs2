import pytest
import base64
import os

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure or execution and attach it to pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        xfail = getattr(report, "wasxfail", False)
        # Capture screenshot if test failed or if passed
        page = item.funcargs.get("page", None)
        if page:
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
                img_src = f"data:image/png;base64,{encoded}"
                
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    html_content = f'''
                    <div style="margin-top: 10px;">
                        <strong>Screenshot:</strong><br/>
                        <img src="{img_src}" 
                             alt="Test Screenshot" 
                             style="width: 300px; max-width: 100%; height: auto; cursor: pointer; border: 2px solid #007bff; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); margin-top: 5px; transition: transform 0.2s;" 
                             onmouseover="this.style.transform='scale(1.02)'"
                             onmouseout="this.style.transform='scale(1)'"
                             onclick="openModal(this.src)" />
                    </div>
                    '''
                    extras.append(pytest_html.extras.html(html_content))
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")

    report.extras = extras


def pytest_html_results_summary(prefix, summary, postfix):
    """
    Inject custom Modal CSS & JS into pytest-html report.
    This fixes the issue where clicking base64 image links opens a blank tab (about:blank) 
    in modern browsers due to top-level data: URL security restrictions.
    """
    prefix.extend([
        r"""
        <style>
            /* Fullscreen Modal Styling */
            .img-modal-overlay {
                display: none;
                position: fixed;
                z-index: 999999;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-color: rgba(0, 0, 0, 0.9);
                backdrop-filter: blur(4px);
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            .img-modal-content {
                max-width: 95vw;
                max-height: 90vh;
                object-fit: contain;
                border-radius: 6px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.8);
                animation: zoomIn 0.25s ease-out;
            }
            @keyframes zoomIn {
                from { transform: scale(0.9); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            .img-modal-close {
                position: absolute;
                top: 20px;
                right: 30px;
                color: #ffffff;
                font-size: 40px;
                font-weight: bold;
                cursor: pointer;
                user-select: none;
                transition: color 0.2s;
            }
            .img-modal-close:hover {
                color: #ff5555;
            }
            .img-modal-caption {
                color: #cccccc;
                margin-top: 12px;
                font-family: sans-serif;
                font-size: 14px;
            }
        </style>


        <div id="imageModalOverlay" class="img-modal-overlay" onclick="closeModal(event)">
            <span class="img-modal-close" onclick="closeModal(event)">&times;</span>
            <img class="img-modal-content" id="modalImageRef" onclick="event.stopPropagation()">
            <div class="img-modal-caption">Click anywhere outside or press ESC to close</div>
        </div>

        <script>
            function openModal(src) {
                var modal = document.getElementById('imageModalOverlay');
                var modalImg = document.getElementById('modalImageRef');
                if (modal && modalImg) {
                    modalImg.src = src;
                    modal.style.display = 'flex';
                    document.body.style.overflow = 'hidden';
                }
            }

            function closeModal(event) {
                var modal = document.getElementById('imageModalOverlay');
                if (modal) {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            }

            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
            });

            // Global click handler to intercept any standard pytest-html screenshot links/thumbnails
            document.addEventListener('click', function(e) {
                var target = e.target;
                
                // If user clicks an image tag inside the report
                if (target.tagName === 'IMG' && target.src && (target.src.startsWith('data:image') || target.src.includes('screenshot'))) {
                    e.preventDefault();
                    e.stopPropagation();
                    openModal(target.src);
                    return false;
                }
                
                // If user clicks an <a> tag linking to a data:image or image file
                var anchor = target.closest('a');
                if (anchor && anchor.href && (anchor.href.startsWith('data:image') || anchor.href.match(/\.(png|jpg|jpeg|webp)$/i))) {
                    e.preventDefault();
                    e.stopPropagation();
                    var childImg = anchor.querySelector('img');
                    openModal(childImg ? childImg.src : anchor.href);
                    return false;
                }
            }, true);
        </script>
        """
    ])
