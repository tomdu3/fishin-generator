from mailer import generate_email_content

def test_snippet():
    print("Testing snippet...")
    html = "<p>Hello</p>"
    url = "http://click.com"
    pixel = "http://open.com/pixel.gif"
    result = generate_email_content(html, url, pixel)
    assert f'<img src="{pixel}"' in result
    assert result.endswith(f' />')
    print("  OK")

def test_full_doc():
    print("Testing full document...")
    html = "<html><body><p>Hello</p></body></html>"
    url = "http://click.com"
    pixel = "http://open.com/pixel.gif"
    result = generate_email_content(html, url, pixel)
    assert f'<img src="{pixel}"' in result
    assert "</body>" in result
    assert result.index(pixel) < result.index("</body>")
    print("  OK")

def test_manual_pixel():
    print("Testing manual pixel...")
    html = '<p>Hello</p><img src="{{ tracking_pixel_url }}">'
    url = "http://click.com"
    pixel = "http://open.com/pixel.gif"
    result = generate_email_content(html, url, pixel)
    assert f'<img src="{pixel}"' in result
    # Count occurrences
    assert result.count(pixel) == 1
    print("  OK")

if __name__ == "__main__":
    test_snippet()
    test_full_doc()
    test_manual_pixel()
    print("\nAll automated tests PASSED!")
