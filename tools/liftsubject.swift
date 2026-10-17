// Usage: swift tools/liftsubject.swift <in.jpg> <out.png>   (People-page portraits: then crop square with sips -c N N --cropOffset Y X)
// Removes the background with Vision's foreground-instance mask (the "lift subject" feature).
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("usage: liftsubject in out.png") }
let inURL = URL(fileURLWithPath: args[1]), outURL = URL(fileURLWithPath: args[2])
guard let ci = CIImage(contentsOf: inURL) else { fatalError("cannot read \(inURL.path)") }

let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ci)
try handler.perform([request])
guard let obs = request.results?.first else { fatalError("no subject found") }
let buffer = try obs.generateMaskedImage(ofInstances: obs.allInstances, from: handler, croppedToInstancesExtent: false)

let ctx = CIContext()
let out = CIImage(cvPixelBuffer: buffer)
guard let cg = ctx.createCGImage(out, from: out.extent, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!),
      let dest = CGImageDestinationCreateWithURL(outURL as CFURL, UTType.png.identifier as CFString, 1, nil)
else { fatalError("cannot write") }
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("instances: \(obs.allInstances.count), wrote \(outURL.path) \(cg.width)x\(cg.height)")
