import InfiniteImageGallery from "../components/infinite_gallery"
import Navbar from "../components/navbar"

export default function Gallery() {
    return (
        <>
            <div className="container" >
                <Navbar/>
                <InfiniteImageGallery url={"/get-images-paginate"}/>
            </div>
        </>
    )
}