#![allow(dead_code)]
use image::codecs::png::PngEncoder;
use image::ColorType;
use image::ImageEncoder;
use std::fs::File;

const WIDTH: u32 = 256;
const HEIGHT: u32 = 256;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (w, h) = (WIDTH, HEIGHT);
    let mut buf = vec![0u8; (w * h * 4) as usize]; // RGBA, 8-bit each

    // Fill the buffer: simple gradient with solid alpha
    for y in 0..h {
        for x in 0..w {
            let i = ((y * w + x) * 4) as usize;
            buf[i + 0] = x as u8;
            buf[i + 1] = y as u8;
            buf[i + 2] = x as u8;
            buf[i + 3] = 255;
        }
    }

    let start = Point { x: 0, y: 0 };
    let end = Point { x: 50, y: 200 };
    draw_line(&mut buf, start, end, Color::BLACK);  

    std::fs::create_dir_all("build/")?;
    let file = File::create("build/out.png")?;
    let encoder = PngEncoder::new(file);
    encoder
        .write_image(&buf, w, h, ColorType::Rgba8.into())
        .unwrap();

    Ok(())
}

pub struct Point {
    pub x: u32,
    pub y: u32,
}

#[derive(Clone, Copy, Eq, PartialEq)]
pub struct Color {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

#[rustfmt::skip]
impl Color {
    const RED: Color = Color { r: 255, g: 0, b: 0, a: 255 };
    const GREEN: Color = Color { r: 0, g: 255, b: 0, a: 255 };
    const BLUE: Color = Color { r: 0, g: 0, b: 255, a: 255 };
    const WHITE: Color = Color { r: 255, g: 255, b: 255, a: 255 };
    const BLACK: Color = Color { r: 0, g: 0, b: 0, a: 255 };

    fn to_u32(&self) -> u32 {
        ((self.r as u32) << 24) |
        ((self.g as u32) << 16) |
        ((self.b as u32) <<  8) |
        ((self.a as u32) <<  0)
    }
}

fn draw_line(buf: &mut [u8], start: Point, end: Point, color: Color) {
    let dx = end.x - start.x;
    let dy = end.y - start.y;
    if dy < dx {
        draw_line_horizontal(buf, start, end, color);
    } else {
        draw_line_vertical(buf, start, end, color);
    }
}

fn draw_line_horizontal(buf: &mut [u8], start: Point, end: Point, color: Color) {
    let dx = end.x - start.x;
    let dy = end.y - start.y;
    let m: f32 = dy as f32 / dx as f32;

    for i in 0..dx {
        let p = Point {
            x: start.x + i,
            y: start.y + (((i as f32) * m) as u32),
        };
        put_pixel(buf, p, color);
    }
}

fn draw_line_vertical(buf: &mut [u8], start: Point, end: Point, color: Color) {
    let dy = end.y - start.y;
    let dx = end.x - start.x;
    let n: f32 = dx as f32 / dy as f32;

    for i in 0..dy {
        let p = Point {
            x: start.x + (((i as f32) * n) as u32),
            y: start.y + i,
        };
        put_pixel(buf, p, color);
    }
}

#[inline]
fn put_pixel(buf: &mut [u8], p: Point, color: Color) {
    let i = ((p.y * WIDTH + p.x) * 4) as usize;
    buf[i + 0] = color.r;
    buf[i + 1] = color.g;
    buf[i + 2] = color.b;
    buf[i + 3] = color.a;
}
