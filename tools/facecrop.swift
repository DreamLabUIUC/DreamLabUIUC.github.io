// Usage: swift tools/facecrop.swift <in.png> <out.png> [size=600] [scale=2.6] [lift=0.15]
// Crops a square around the largest detected face (macOS Vision) and resizes it, keeping transparency.
// scale = square side as a multiple of the face height; lift = how far below the face centre the square
// is centred, as a fraction of the side (positive moves the crop down to include shoulders).
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 3 else { fatalError("usage: facecrop in out [size] [scale] [lift]") }
let size = a.count > 3 ? Double(a[3])! : 600, scale = a.count > 4 ? Double(a[4])! : 2.6, lift = a.count > 5 ? Double(a[5])! : 0.15
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("cannot read") }
let W = Double(img.width), H = Double(img.height)

let req = VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(cgImage: img).perform([req])
guard let face = (req.results ?? []).max(by: { $0.boundingBox.height < $1.boundingBox.height }) else { fatalError("no face") }
let fb = face.boundingBox  // normalized, origin bottom-left
let fx = (fb.midX) * W, fy = (1 - fb.midY) * H, fh = fb.height * H
var side = min(fh * scale, min(W, H))
var cx = fx, cy = fy + side * lift
var x0 = max(0, min(W - side, cx - side / 2)), y0 = max(0, min(H - side, cy - side / 2))
guard let crop = img.cropping(to: CGRect(x: x0, y: y0, width: side, height: side)) else { fatalError("crop failed") }

let n = Int(size)
let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high
ctx.draw(crop, in: CGRect(x: 0, y: 0, width: n, height: n))
let out = ctx.makeImage()!
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, out, nil)
CGImageDestinationFinalize(dest)
print("face h=\(Int(fh))px, crop side=\(Int(side))px -> \(n)x\(n)")
