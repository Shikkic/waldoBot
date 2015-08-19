//
//  ViewController.swift
//  waldo bot
//
//  Created by Dan Cadden on 7/24/15.
//  Copyright (c) 2015 shikkic. All rights reserved.
//


import UIKit
import Alamofire
import SDWebImage


class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    @IBOutlet var waldo: UIView!
    @IBOutlet weak var imageView: UIImageView!
    
    let imagePicker = UIImagePickerController()

    func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [NSObject : AnyObject]) {
        imagePicker.dismissViewControllerAnimated(true, completion: nil)
        let image = info[UIImagePickerControllerOriginalImage] as? UIImage
        let imageData = UIImagePNGRepresentation(image)
        let paths = NSSearchPathForDirectoriesInDomains(.DocumentDirectory, .UserDomainMask, true)[0] as! String
        let imagePath = paths.stringByAppendingPathComponent("cached.png")
        
        if !imageData.writeToFile(imagePath, atomically: false)
        {
            println("not saved")
        } else {
//            let filePath = NSBundle.mainBundle().pathForResource("cached", ofType: "png")
            let url = NSURL(fileURLWithPath: imagePath);
            println(url)
            Alamofire.upload(
                .POST,
                URLString: "http://356ee014.ngrok.com",
                multipartFormData: { multipartFormData in
                    multipartFormData.appendBodyPart(fileURL: url!, name: "file")
                },
                encodingCompletion: { encodingResult in
                    switch encodingResult {
                    case .Success(let upload, _, _):
                        upload.responseJSON { request, response, JSON, error in
                            println(JSON)
                            println(response)
                            println(request)
                            let cache = SDImageCache.sharedImageCache();
                            cache.clearDisk()
                            cache.clearMemory()
                            self.imageView.sd_setImageWithURL(NSURL(string: "http://356ee014.ngrok.com/result/cached.png"))
                        }
                        println("IT WORKED ME")
                        
                    case .Failure(let encodingError):
                        println(encodingError)
                    }
                }
            )
        }
        print("request was laumched")
        
    }
    
    @IBAction func picture(sender: AnyObject) {
        if UIImagePickerController.isCameraDeviceAvailable( UIImagePickerControllerCameraDevice.Front) {
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.Camera
            presentViewController(imagePicker, animated: true, completion: nil)
            print(imagePicker)
        } else {
            print("error no camera")
        }
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        print("Did this load?")
        // Do any additional setup after loading the view, typically from a nib.
       
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

