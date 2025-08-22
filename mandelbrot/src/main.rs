use image::ImageBuffer;
use image::RgbaImage;
use anyhow::anyhow;
use num_complex::Complex;

const IMG_WIDTH: u32 = 800;
const IMG_HEIGHT: u32 = 600;
const ASPECT: f32 = (IMG_WIDTH as f32) / (IMG_HEIGHT as f32);

const Z_WIDTH: f32 = 3.0;
const Z_HEIGHT: f32 = Z_WIDTH / ASPECT;

fn main() -> anyhow::Result<()> {
    let mut buf: Vec<u8> = vec![0; (IMG_WIDTH * IMG_HEIGHT * 4) as usize];

    let mut x = 0;
    let mut y = 0;
    for i in (0..buf.len()).step_by(4) {
        let c = image_to_world(x, y);

        let z = mandelbrot_iter(c);
        let intensity = sigmoid(z.norm());
        let brightness = ((intensity * 256.0) as u8).min(255);
        buf[i + 0] = brightness;
        buf[i + 1] = brightness;
        buf[i + 2] = brightness;
        buf[i + 3] = 255;

        x += 1;
        if x == IMG_WIDTH {
            x = 0;
            y += 1;
        }
    }

    let img: RgbaImage = ImageBuffer::from_raw(IMG_WIDTH, IMG_HEIGHT, buf)
        .ok_or_else(|| anyhow!("Error"))?;

    std::fs::create_dir_all("build/")?;
    img.save("build/mandelbrot.png")?;

    Ok(())
}

fn image_to_world(x: u32, y: u32) -> Complex<f32> {
    let z_real = (x as f32 / IMG_WIDTH as f32) * Z_WIDTH - Z_WIDTH / 2.0;
    let z_imag = (y as f32 / IMG_HEIGHT as f32) * Z_HEIGHT - Z_HEIGHT / 2.0;

    Complex::new(z_real, z_imag)
}

fn mandelbrot_iter(c: Complex<f32>) -> Complex<f32> {
    let mut z = Complex::new(0f32, 0f32);
    for _i in 0..100 {
        z = z * z + c;
    }
    z
}

fn sigmoid(x: f32) -> f32 {
    1.0 / (1.0 + (-x).exp())
}
