import {PureComponent} from 'react';
import axios from "axios";
import { v4 as uuid } from 'uuid';
import ReactCrop from 'react-image-crop';
import { Button } from 'antd';
import 'react-image-crop/dist/ReactCrop.css';

interface IAppProps {
}

function dataURItoBlob(dataURI) {
  // convert base64 to raw binary data held in a string
  // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
  var byteString = atob(dataURI.split(',')[1]);

  // separate out the mime component
  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]

  // write the bytes of the string to an ArrayBuffer
  var ab = new ArrayBuffer(byteString.length);

  // create a view into the buffer
  var ia = new Uint8Array(ab);

  // set the bytes of the buffer to the correct values
  for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
  }

  // write the ArrayBuffer to a blob, and you're done
  var blob = new Blob([ab], {type: mimeString});
  return blob;

}


interface IAppState {
  src: any;
  srcType: any;
  image: any;
  crop: any;
  output: any;
  resultName: string;
  file: any;
  token: any;
}

class App extends PureComponent<IAppProps, IAppState> {
	state = {
		src: null,
		srcType: null,
		crop: { aspect: 16 / 9 },
		image: null,
		output: null,
		resultName: '',
		file: null,
		token: null
	};

	selectImage = async (file) => {
		console.log(file);
		const x = URL.createObjectURL(file);
		console.log(x);
		this.setState({
			src: x,
			srcType: file.type
		})
		console.log(this.state.src);
	};

	handleVkResponse = (data) => {
		console.warn(data)
	}

	cropImageNow = () => {
		const image = this.state.image
		const crop = this.state.crop
		const type = this.state.srcType
		const canvas = document.createElement('canvas');
		const scaleX = image.naturalWidth / image.width;
		const scaleY = image.naturalHeight / image.height;
		canvas.width = crop.width;
		canvas.height = crop.height;
		const ctx = canvas.getContext('2d');

		const pixelRatio = window.devicePixelRatio;
		canvas.width = crop.width * pixelRatio;
		canvas.height = crop.height * pixelRatio;
		ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
		ctx.imageSmoothingQuality = 'high';
		console.log(image)
		ctx.drawImage(
			image,
			crop.x * scaleX,
			crop.y * scaleY,
			crop.width * scaleX,
			crop.height * scaleY,
			0,
			0,
			crop.width,
			crop.height,
		);

		// Converting to base64
		const resultName = uuid();
		const base64Image = canvas.toDataURL(type);
		axios.post("http://localhost:5000/save-image", {name: resultName, file: base64Image.replace('data:'+type+';base64,', ''), type: type}).then(() => {
			console.log('saved as ' + resultName)
		})
		this.setState({output: base64Image, resultName: resultName})
};

	getImage = async (fileName, fileType) => {
		axios.get("http://localhost:5000/image?name="+fileName+"&type="+fileType).then(response => {
        console.log(response);
		this.setState({file: response.data})
      }).catch(function(error) {
        console.log(error);
      });
	};

	setToken = (token) => {
		this.setState({token: token})
	}
	sendImage = async (fileName, fileType, token) => {
		await axios.post("http://localhost:5000/post-image?name=" + fileName + "&type=" + fileType + "&token=" + token).then(()=>{
			console.log('ok')
		})

	}

	render() {
		const token=window.location.href.split('#')
		if (token[1]) {
			return <div className="App">
				<center>
					paste this into previous tab
					<br/>
					{token[1].split('&')[0].split('=')[1]}
				</center>
			</div>
		}
		const {src, crop, output, resultName, srcType, file} = this.state
		if (output) {
			const token=window.location.href.split('#')
			console.log(token)
		}
		return (
				<div className="App">
				<center>
					<input
					type="file"
					accept="image/*"
					onChange={(e) => {
						this.selectImage(e.target.files[0]);
					}}
					/>
					<br />
					<br />
					<div>
					{src && (
						<div>
						<ReactCrop crop={crop} onChange={(c) => {this.setState({crop: c})}}>
							<img
								   src={src}
								   onLoad={(i) => {this.setState({image: i.target})}}
								/>
							</ReactCrop>
						<br />
						<button onClick={this.cropImageNow}>Crop</button>
						<br />
						<br />
						</div>
					)}
					</div>
					<div>{output && <img alt={resultName} src={output} />}</div>
					{output  &&
						<a href={output} download="crop_result" target='_blank'>
							<button type="button">Download cropped image</button>
						</a>
					}
					{output  &&
					<a target='_blank' href="https://oauth.vk.com/authorize?client_id=8001067&display=page&redirect_uri=localhost:3001&scope=photos,wall&response_type=token&v=5.131&state=123456" >
						<button type="button">Auth in VK</button>
					</a>
					}
					{output  &&
					<input id="token"
						   onChange={(e) => {
						this.setToken(e.target.value);}}
					/>
					}
					{output  &&
					<Button onClick={()=>{this.sendImage(resultName, srcType, this.state.token)}}>Default Button</Button>
					}
				</center>
				</div>
			);
	}
}

export default App;