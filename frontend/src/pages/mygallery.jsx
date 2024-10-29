import InfiniteImageGallery from "../components/infinite_gallery"
import Navbar from "../components/navbar"

export default function MyGallery() {
    return (
        <>
            <div className="container">
                <Navbar/>
                <InfiniteImageGallery url={"/get-user-images-paginate"}/>
            </div>
        </>
    )
}