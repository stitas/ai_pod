import InfiniteImageGallery from "../components/infinite_gallery"
import Navbar from "../components/navbar"

export default function Gallery() {
    return (
        <>
            <div className="container" >
                <Navbar name=""/>
                <InfiniteImageGallery url={"/get-images-paginate/"}/>
            </div>
        </>
    )
}